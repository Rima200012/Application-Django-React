from django.views import View
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
import fitz  # PyMuPDF
from gensim.models import Word2Vec
from scipy import spatial
import re
from AI.utils_clustering import perform_kmeans_clustering, calculate_metrics
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import time

# Import the preprocessing functions
from .utils import (
    get_resume_content,
    get_text_from_pdf,
    preprocess_text,
    avg_feature_vector,
    compare_two_list_skills_avg,
    get_word_vectors
)

# Connect to MongoDB
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Function to extract personal information from CV
def extract_info_from_cv(cv_text):
    info = {}

    # Extract Name (Assuming the first line is the name)
    name_match = re.search(r'^[A-Za-z\s\-]+$', cv_text, re.MULTILINE)
    if name_match:
        info['Name'] = name_match.group().strip()

    # Extract Email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', cv_text)
    if email_match:
        info['Email'] = email_match.group().strip()

    # Extract Phone Number
    phone_match = re.search(r'\+216\s?\d{2}\s?\d{3}\s?\d{3}', cv_text)
    if phone_match:
        info['Phone'] = phone_match.group().strip()

    # Extract Address (Basic regex for street address)
    address_match = re.search(r'Adresse[:\s]+(.*?)(?=\s*[\n]|$)', cv_text, re.IGNORECASE)
    if address_match:
        info['Address'] = address_match.group(1).strip()
    else:
        # Additional attempt to find address in a different format
        address_match_alt = re.search(r'\bTunisie,?(.*?)(?=\s*[\n]|$)', cv_text, re.IGNORECASE)
        if address_match_alt:
            info['Address'] = address_match_alt.group(1).strip()

    # Extract Nationality
    nationality_match = re.search(r'\b[Tt]unisienne\b', cv_text)
    if nationality_match:
        info['Nationality'] = nationality_match.group().strip()

    # Extract LinkedIn URL
    linkedin_match = re.search(r'linkedin\.com/in/[A-Za-z0-9\-]+', cv_text)
    if linkedin_match:
        info['LinkedIn'] = linkedin_match.group().strip()

    return info

class ResumeSimilarityView(View):
    def get(self, request, job_post_id):
        try:
            # Check if recommendations already exist for this job post
            existing_recommendation = db['recommended_candidates'].find_one({"job_post_id": ObjectId(job_post_id)})
            if existing_recommendation:
                return JsonResponse(existing_recommendation['recommendations'], safe=False)

            # Fetch the job description from the database
            job_post = db['job_posts'].find_one({"_id": ObjectId(job_post_id)})
            if not job_post:
                return JsonResponse({"error": "Job post not found"}, status=404)
            
            job_description = job_post['description']
            cleaned_job_description = preprocess_text(job_description)

            # Fetch all resumes from the database
            resumes = db['job_applications'].find()
            results = []

            # Load pre-trained Word2Vec model
            model = Word2Vec.load('models/word2vec_cbow_model.bin')

            for resume in resumes:
                resume_id = resume['_id']
                resume_content = get_resume_content(resume['resume'])
                resume_text = get_text_from_pdf(resume_content)
                cleaned_resume_text = preprocess_text(resume_text)

                # Calculate similarity score between job description and resume
                similarity_score = compare_two_list_skills_avg(cleaned_job_description, cleaned_resume_text, model)

                # Extract personal information from the CV
                personal_info = extract_info_from_cv(resume_text)

                results.append({
                    "resume_id": str(resume_id),
                    "similarity_score": similarity_score,
                    "name": personal_info.get('Name', 'N/A'),
                    "email": personal_info.get('Email', 'N/A')
                })

            # Sort the results by cosine similarity score in descending order
            results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)

            # Select the top 10 results
            top_matches = results[:10]

            # Save the top 10 recommendations to the MongoDB collection
            db['recommended_candidates'].insert_one({
                "job_post_id": ObjectId(job_post_id),
                "recommendations": top_matches,
                "timestamp": time.time()
            })

            # Return the top 10 recommendations
            return JsonResponse(top_matches, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class EvaluateKMeansView(View):
    def get(self, request, *args, **kwargs):
        # Get the resumes and job description vectors
        resumes = db['job_applications'].find()
        job_post = db['job_posts'].find_one({"_id": ObjectId("669405cf0f6ad4fffd730691")})


        if not job_post:
            return JsonResponse({"error": "Job post not found"}, status=404)

        job_desc_vector = get_word_vectors(preprocess_text(job_post['description']).split())
        
        resume_vectors = []
        resume_ids = []

        for resume in resumes:
            resume_text = get_text_from_pdf(get_resume_content(resume['resume']))
            resume_vector = get_word_vectors(preprocess_text(resume_text).split())
            resume_vectors.append(resume_vector)
            resume_ids.append(str(resume['_id']))

        # Convert the list of vectors to a NumPy array
        X = np.array(resume_vectors)

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=4, init='random', max_iter=100)
        kmeans.fit(X)

        labels = kmeans.labels_
        inertia = kmeans.inertia_
        silhouette_avg = silhouette_score(X, labels)
        calinski_harabasz = calinski_harabasz_score(X, labels)
        davies_bouldin = davies_bouldin_score(X, labels)

        # Convert metrics to standard Python data types
        metrics = {
            "inertia": float(inertia),
            "silhouette_score": float(silhouette_avg),
            "calinski_harabasz_score": float(calinski_harabasz),
            "davies_bouldin_score": float(davies_bouldin)
        }

        # Add resume IDs and their clusters to the response
        clustered_resumes = []
        for i, resume_id in enumerate(resume_ids):
            clustered_resumes.append({
                "resume_id": resume_id,
                "cluster": int(labels[i])  # Convert label to a standard int
            })

        return JsonResponse({
            "metrics": metrics,
            "clustered_resumes": clustered_resumes
        })
    




class LastSavedRecommendationsView(View):
    def get(self, request, job_post_id):
        try:
            # Fetch the last saved recommendations for the job post
            recommendation = db['recommended_candidates'].find_one({"job_post_id": ObjectId(job_post_id)}, sort=[("timestamp", -1)])
            
            if not recommendation:
                return JsonResponse({"error": "No recommendations found for this job post"}, status=404)

            # Return the saved recommendations
            return JsonResponse(recommendation['recommendations'], safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)