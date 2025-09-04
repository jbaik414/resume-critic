import pandas as pd
from sentence_transformers import SentenceTransformer, util
import spacy
from .pdf_parser import extract_text_from_pdf
import os

embedder = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "job_title_des.csv")

df = pd.read_csv(csv_path)


def extract_keywords(text):
    doc = nlp(text)
    return set([ent.text for ent in doc.ents if ent.label_ in ["ORG","PRODUCT","GPE","SKILL"]])

def critique_resume(pdf_path, top_k=3):
    resume_text = extract_text_from_pdf(pdf_path)

    job_embeddings = embedder.encode(df["Job Description"].tolist(), convert_to_tensor=True)
    resume_embedding = embedder.encode(resume_text, convert_to_tensor=True)

    cos_scores = util.pytorch_cos_sim(resume_embedding, job_embeddings)[0]
    top_results = cos_scores.topk(k=top_k)

    feedback = []
    for score, idx in zip(top_results[0], top_results[1]):
        idx = int(idx)
        job_title = df.iloc[idx]["Job Title"]
        job_desc = df.iloc[idx]["Job Description"]

        job_keywords = extract_keywords(job_desc)
        resume_keywords = extract_keywords(resume_text)
        missing = job_keywords - resume_keywords

        feedback.append({
            "job_title": job_title,
            "match_score": round(score.item(), 3),
            "missing_keywords": list(missing)[:5]
        })
    return feedback
