import os
import sys
import time
from gensim.models import Word2Vec
from pymongo import MongoClient
from django.conf import settings

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

# Import Django app modules
from AI.utils import preprocess_text, get_resume_content, get_text_from_pdf

# Connect to MongoDB
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

def create_model_CBOW(corpus, modelFile):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(modelFile), exist_ok=True)
    
    start = time.time()
    print("Training model...")
    model = Word2Vec(corpus, vector_size=100, workers=2, min_count=5, sg=0)  # sg=0 for CBOW
    model.save(modelFile)
    end = time.time()
    print("Took %s seconds" % (end - start))

if __name__ == "__main__":
    # Fetch and preprocess resumes to build the corpus
    resumes = db['job_applications'].find()
    corpus = []

    for resume in resumes:
        resume_content = get_resume_content(resume['resume'])  # Fetch content from GridFS or another source
        resume_text = get_text_from_pdf(resume_content)  # Extract text from PDF
        cleaned_resume_text = preprocess_text(resume_text)
        corpus.append(cleaned_resume_text.split())  # Tokenized text

    # Train the Word2Vec model and save it
    create_model_CBOW(corpus, 'models/word2vec_cbow_model.bin')
