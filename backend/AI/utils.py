from pymongo import MongoClient
from bson import ObjectId
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

import gensim
from gensim.models import Word2Vec
import numpy as np
from scipy.spatial import distance
import fitz  # PyMuPDF
import time
import logging
from scipy import spatial


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from django.conf import settings
import gridfs
from pdfminer.high_level import extract_text
from io import BytesIO


# Initialisation de la connexion à MongoDB
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
fs = gridfs.GridFS(db)

# Pipeline de prétraitement des données
def to_lowercase(s):
    return s.lower()

def nettoyage_text_espaces(s):
    s = s.replace(' \n', '')
    s = s.replace(' / ',' ')
    t = s.split(" ")
    while len(t) > 1:
        s = s.replace("  ", " ")
        t = s.split("  ")
    return s.lstrip()

def supp_caractere_speciaux(s):
     # Suppression des URLs
     s = re.sub(r'http\S+', '', s, flags=re.MULTILINE)
    
     # Suppression des hashtags, @ et $
     s = s.replace('#', '').replace('@', '').replace('$', '')
    
     # Conserver les accents, apostrophes, traits d'union et autres caractères français
     s = re.sub(r'[^\w\s\'éèàçùôêî\-]', '', s)
    
     # Suppression des chiffres (si nécessaire)
     s = re.sub(r'\d+', '', s)
    
     # Remplacement des retours à la ligne et tabulations par des espaces
     s = s.replace('\n', ' ').replace('\t', ' ')
    
     # Suppression des espaces multiples
     s = re.sub(r'\s+', ' ', s).lstrip()
    
     return s




def supp_stop_words(s, language='french'):
    # Définir les caractères de ponctuation à supprimer, en excluant les apostrophes et traits d'union
    punctuation_tokens = set(('. , - ! ; ? ) : (').split())
    
    # Tokenisation
    tokens = word_tokenize(s)
    
    # Charger les stopwords
    stop_words_set = set(stopwords.words(language))
    
    # Filtrer les tokens pour supprimer les stopwords et la ponctuation
    filtered_text = [t for t in tokens if not(t in stop_words_set or t in punctuation_tokens)]
    
    return ' '.join(filtered_text)

def return_stem(s, language='french'):
    stemmer = SnowballStemmer(language=language)
    tokens = word_tokenize(s)
    stemmed_text = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_text)

def preprocess_text(text):
    start_time = time.time()
    text = to_lowercase(text)
    logging.info(f"Time for to_lowercase: {time.time() - start_time} seconds")
    
    start_time = time.time()
    text = nettoyage_text_espaces(text)
    logging.info(f"Time for nettoyage_text_espaces: {time.time() - start_time} seconds")
    
    start_time = time.time()
    #text = supp_caractere_speciaux(text)
    logging.info(f"Time for supp_caractere_speciaux: {time.time() - start_time} seconds")
    
    start_time = time.time()
    text = supp_stop_words(text, 'french')
    logging.info(f"Time for supp_stop_words (French): {time.time() - start_time} seconds")
    
    start_time = time.time()
    text = supp_stop_words(text, 'english')
    logging.info(f"Time for supp_stop_words (English): {time.time() - start_time} seconds")
    
    start_time = time.time()
    text = return_stem(text, 'french')
    logging.info(f"Time for return_stem: {time.time() - start_time} seconds")
    
    return text

# Fonction pour récupérer le contenu d'un CV depuis GridFS
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
            with fitz.open(stream=file_data, filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            return text.replace('ân¢', '-').replace('ânn', '-')
        except Exception as e:
            print("Error extracting text:", e)
            return ''
    return ''

def preprocess_and_store_cv(cv_file_id):
    start_time = time.time()
    logging.info(f"Start processing CV with ID: {cv_file_id}")
    
    try:
        resume_content = get_resume_content(ObjectId(cv_file_id))
        logging.info(f"Time to fetch resume content: {time.time() - start_time} seconds")
        
        if not resume_content:
            raise ValueError("Resume file not found or empty")
        
        text_start_time = time.time()
        resume_text = get_text_from_pdf(resume_content)
        logging.info(f"Time to extract text from PDF: {time.time() - text_start_time} seconds")

        if not resume_text:
            raise ValueError("No text extracted from resume")

        preprocess_start_time = time.time()
        cleaned_text = preprocess_text(resume_text)
        logging.info(f"Time for preprocessing text: {time.time() - preprocess_start_time} seconds")

        db['job_applications'].update_one(
            {"_id": ObjectId(cv_file_id)},
            {"$set": {"cleaned_resume": cleaned_text}}
        )
        logging.info(f"Total time for processing CV with ID {cv_file_id}: {time.time() - start_time} seconds")

        return cleaned_text
    
    except Exception as e:
        raise RuntimeError(f"Error processing CV with ID {cv_file_id}: {e}")



def create_model_CBOW(corpus, modelFile):
    start = time.time()
    print("Training model...")
    model = Word2Vec(corpus, vector_size=100, window=5, min_count=1, workers=4, sg=0)  # sg=0 is for CBOW
    model.save(modelFile)
    end = time.time()
    print("Took %s seconds" % (end - start))

def load_model(modelFile):
    return Word2Vec.load(modelFile)

def avg_feature_vector(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0
    index2word_set = set(model.wv.index_to_key)
    
    for word in words:
        if word in index2word_set:
            nwords += 1
            featureVec = np.add(featureVec, model.wv[word])
    
    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    
    return featureVec

def compare_two_list_skills_avg(skills_1, skills_2, model):
    sentence_1_avg_vector = avg_feature_vector(skills_1.split(), model, num_features=100)
    sentence_2_avg_vector = avg_feature_vector(skills_2.split(), model, num_features=100)
    
    similarity = 1 - distance.cosine(sentence_1_avg_vector, sentence_2_avg_vector)
    return similarity

def compare_resume_with_job(cv_file_id, job_post_id, model):
    try:
        resume_content = get_resume_content(ObjectId(cv_file_id))
        resume_text = get_text_from_pdf(resume_content)
        cleaned_resume_text = preprocess_text(resume_text)
        
        job_post = db['job_posts'].find_one({"_id": ObjectId(job_post_id)})
        if not job_post:
            raise ValueError("Job post not found")
        job_description = job_post.get('description', '')
        cleaned_job_description = preprocess_text(job_description)
        
        similarity_score = compare_two_list_skills_avg(cleaned_resume_text, cleaned_job_description, model)
        
        return similarity_score
    
    except Exception as e:
        print(f"Error comparing resume with job description: {e}")
        return None

def get_word_vectors(words):
    model = Word2Vec.load('models/word2vec_cbow_model.bin')
    num_features = model.vector_size
    feature_vector = np.zeros((num_features,), dtype="float32")
    nwords = 0

    index2word_set = set(model.wv.index_to_key)
    
    for word in words:
        if word in index2word_set:
            nwords += 1
            feature_vector = np.add(feature_vector, model.wv[word])
    
    if nwords > 0:
        feature_vector = np.divide(feature_vector, nwords)
    
    return feature_vector