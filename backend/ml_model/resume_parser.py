import spacy
import pandas as pd
from pdfminer.high_level import extract_text
import re
from typing import Dict, Any
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    return extract_text(pdf_path)

def preprocess_text(text: str) -> str:
    """Preprocess text by removing special characters, stopwords, etc."""
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    
    return ' '.join(filtered_text)

def extract_skills(text: str) -> list:
    """Extract skills from text using Spacy NER"""
    doc = nlp(text)
    skills = []
    
    # Extract noun chunks that might represent skills
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Avoid long phrases
            skills.append(chunk.text)
    
    # Also look for specific entities
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            skills.append(ent.text)
    
    return list(set(skills))  # Remove duplicates

def extract_experience(text: str) -> list:
    """Extract work experience information"""
    # This is a simplified version - in a real app you'd use more sophisticated parsing
    experience = []
    lines = text.split('\n')
    
    # Look for patterns indicating experience sections
    for i, line in enumerate(lines):
        if "experience" in line.lower():
            # Try to extract the next few lines as experience
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip():
                    experience.append(lines[j].strip())
    
    return experience

def extract_education(text: str) -> list:
    """Extract education information"""
    education = []
    lines = text.split('\n')
    
    # Look for patterns indicating education sections
    for i, line in enumerate(lines):
        if "education" in line.lower():
            # Try to extract the next few lines as education
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip():
                    education.append(lines[j].strip())
    
    return education

def calculate_keyword_scores(text: str, keywords: list) -> dict:
    """Calculate TF-IDF scores for given keywords in the text"""
    vectorizer = TfidfVectorizer(vocabulary=keywords)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
    return scores

def parse_resume(file_path: str) -> Dict[str, Any]:
    """Main function to parse resume and return structured data"""
    try:
        raw_text = extract_text_from_pdf(file_path)
        processed_text = preprocess_text(raw_text)
        
        result = {
            "skills": extract_skills(processed_text),
            "experience": extract_experience(raw_text),
            "education": extract_education(raw_text),
            "raw_text": raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text,
            "processed_text": processed_text[:1000] + "..." if len(processed_text) > 1000 else processed_text,
        }
        
        # Example keyword analysis (in a real app, you'd have a more comprehensive list)
        tech_keywords = ["python", "java", "javascript", "sql", "machine learning", "ai"]
        keyword_scores = calculate_keyword_scores(processed_text, tech_keywords)
        result["keyword_scores"] = keyword_scores
        
        return result
    except Exception as e:
        raise Exception(f"Error parsing resume: {str(e)}")