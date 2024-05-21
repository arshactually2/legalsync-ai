from fastapi import FastAPI, UploadFile, File
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

@app.post("/assess")
async def assess_risk(file: UploadFile = File(...)):
    content = await file.read()
    document = content.decode("utf-8")
    risk_score, risk_factors = analyze_document(document)
    return {"risk_score": risk_score, "risk_factors": risk_factors}

def analyze_document(document):
    doc = nlp(document)
    risk_factors = []
    for sentence in doc.sents:
        if "may" in sentence.text or "could" in sentence.text:
            risk_factors.append(sentence.text)
    risk_score = len(risk_factors) / len(list(doc.sents))
    return risk_score, risk_factors
