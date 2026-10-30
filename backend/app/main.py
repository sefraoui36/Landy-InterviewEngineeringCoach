from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.llm import get_llm
from app.parsing.pdf import parse_pdf
from app.extraction.extractor import extraire_profil_cv
import os
from app.interview.engine import generer_plan_entretien
load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Landy API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "agent": "Landy", "version": "0.1.0"}

@app.get("/llm/test")
def test_llm():
    try:
        llm = get_llm()
        reponse = llm.generate(
            prompt="Dis 'Bonjour, je suis Landy' en une seule phrase courte.",
            system_prompt="Tu es un assistant utile."
        )
        return {"llm_response": reponse}
    except Exception as e:
        return {"error": str(e)}

@app.get("/parse/test")
def test_parsing():
    try:
        pdf_path = "../data/test_cv.pdf"
        if not os.path.exists(pdf_path):
            return {"error": "Fichier introuvable."}
        extracted_text = parse_pdf(pdf_path)
        return {"status": "success", "chars_extracted": len(extracted_text)}
    except Exception as e:
        return {"error": str(e)}

# --- C'EST ICI QUE CA SE JOUE ---
@app.get("/extract/test")
def test_extraction():
    try:
        pdf_path = "../data/test_cv.pdf"
        texte_brut = parse_pdf(pdf_path)
        profil_json = extraire_profil_cv(texte_brut)
        return {"status": "success", "profil": profil_json}
    except Exception as e:
        return {"error": str(e)}
# --------------------------------
@app.get("/interview/plan")
def test_plan_entretien():
    try:
        # 1. On lit le PDF
        pdf_path = "../data/test_cv.pdf"
        texte_brut = parse_pdf(pdf_path)

        # 2. On extrait le JSON
        profil_json = extraire_profil_cv(texte_brut)

        # 3. On génère le plan d'entretien
        plan = generer_plan_entretien(profil_json)

        return {"status": "success", "plan": plan}
    except Exception as e:
        return {"error": str(e)}