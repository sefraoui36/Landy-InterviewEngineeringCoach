from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.llm import get_llm
from app.parsing.pdf import parse_pdf
from app.extraction.extractor import extraire_profil_cv
import os
from app.interview.engine import generer_plan_entretien
from app.storage.db import init_db, SessionLocal, DBSession
from app.interview.session import InterviewSession
from pydantic import BaseModel
load_dotenv(dotenv_path="../.env")
app = FastAPI(title="Landy API", version="0.1.0")
init_db()
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


class UserResponse(BaseModel):
    reponse: str


# Variable globale temporaire (on utilisera une base de données plus tard)
current_session = None


@app.post("/interview/start")
def start_interview():
    db = SessionLocal()
    try:
        pdf_path = "../data/test_cv.pdf"
        texte_brut = parse_pdf(pdf_path)
        profil_json = extraire_profil_cv(texte_brut)
        plan = generer_plan_entretien(profil_json)

        # 1. Création de la session en base
        db_session = DBSession(
            plan_json=plan,
            history_json=[],
            current_index=0
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        # 2. On garde aussi la session en mémoire pour la suite
        global current_session
        current_session = InterviewSession(plan)

        return {
            "status": "success",
            "session_id": db_session.id,  # <-- NOUVEAU : L'ID de la session en base
            "question_actuelle": current_session.get_current_question(),
            "progression": f"1 / {len(current_session.questions)}"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@app.post("/interview/answer")
def answer_interview(data: UserResponse):
    global current_session
    if not current_session:
        return {"error": "Aucun entretien en cours. Appelle /interview/start d'abord."}

    # 1. Enregistrer la réponse
    current_session.add_user_response(data.reponse)

    # 2. Vérifier si c'est terminé
    if current_session.current_index >= len(current_session.questions):
        return {
            "status": "finished",
            "message": "L'entretien est terminé !",
            "history": current_session.history
        }

    # 3. Sinon, poser la question suivante
    return {
        "status": "success",
        "question_actuelle": current_session.get_current_question(),
        "progression": f"{current_session.current_index + 1} / {len(current_session.questions)}"
    }