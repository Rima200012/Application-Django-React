from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pymongo import MongoClient
from django.conf import settings
from io import BytesIO
import gridfs
from pdfminer.high_level import extract_text
import re
from concurrent.futures import ThreadPoolExecutor

# MongoDB Setup
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
fs = gridfs.GridFS(db)

class Resume:
    collection = db['fs.files']

    @staticmethod
    def find_all():
        return Resume.collection.find()

def get_resume_content(file_id):
    try:
        file = fs.get(file_id)
        return file.read()
    except Exception as e:
        print("Error retrieving file:", e)
        return None

def get_text_from_pdf(file_data):
    if file_data:
        try:
            text = extract_text(BytesIO(file_data))
            return text.replace('ân¢', '-').replace('ânn', '-')
        except Exception as e:
            print("Error extracting text:", e)
            return ''
    return ''

def process_resume(file_id):
    try:
        resume_content = get_resume_content(file_id)
        resume_text = get_text_from_pdf(resume_content)
        return str(file_id), resume_text
    except Exception as e:
        print(f"Error processing resume with ID {file_id}: {e}")
        return None, None

def calculate_similarity(job_description, resumes):
    documents = [job_description] + resumes
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)  # Debugging statement
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    print("Cosine Similarities:", cosine_similarities)  # Debugging statement
    return cosine_similarities

def recommend_candidates(job_description):
    resume_files = Resume.find_all()
    resume_ids = []
    resumes = []

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_resume, resume_file['_id']) for resume_file in resume_files]
        for future in futures:
            resume_id, resume_text = future.result()
            if resume_id and resume_text:
                resume_ids.append(resume_id)
                resumes.append(resume_text)

    print("Job Description:\n", job_description)  # Print job description for context
    print("Resumes retrieved:", len(resumes))  # Debugging statement

    if not resumes:
        return []

    cosine_similarities = calculate_similarity(job_description, resumes)
    similarity_scores = list(zip(resume_ids, cosine_similarities))

    print("Cosine Similarities and IDs:")
    for score in similarity_scores:
        print(f"Resume ID: {score[0]}, Similarity Score: {score[1]}")  # Debugging statement

    # Filter results by a similarity score threshold, e.g., 0.1
    filtered_scores = [score for score in similarity_scores if score[1] > 0.1]
    print("Filtered Scores (after threshold):")
    for score in filtered_scores:
        print(f"Resume ID: {score[0]}, Similarity Score: {score[1]}")  # Debugging statement

    if not filtered_scores:
        print("No scores above threshold. Returning empty recommendations.")
        return []

    filtered_scores.sort(key=lambda x: x[1], reverse=True)
    top_matches = filtered_scores[:10]

    recommendations = [{"resume_id": match[0], "similarity_score": match[1]} for match in top_matches]
    print("Top Matches (sorted and filtered):", recommendations)  # Debugging statement

    return recommendations
