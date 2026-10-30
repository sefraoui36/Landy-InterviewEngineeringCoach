import json
from app.llm import get_llm
from app.interview.schemas import PlanEntretien


def generer_plan_entretien(profil_cv: dict) -> dict:
    llm = get_llm()

    # On transforme le dict Python en belle chaîne JSON pour le prompt
    profil_str = json.dumps(profil_cv, ensure_ascii=False, indent=2)

    prompt = f"""
    Tu es un recruteur technique. Voici le profil JSON d'un candidat :
    {profil_str}

    Génère un plan d'entretien de 5 questions.
    - Commence par une question sur son projet le plus complexe.
    - Pose une question technique sur une de ses compétences.
    - Pose une question comportementale (ex: gestion d'un échec).
    - Termine par une question sur sa motivation.
    Pour chaque question, précise la compétence ciblée, le type, et le but du recruteur.
    """

    schema_dict = PlanEntretien.model_json_schema()

    reponse_json_str = llm.generate(
        prompt=prompt,
        system_prompt="Tu es un expert en entretien d'embauche pour ingénieurs. Tu poses des questions exigeantes mais bienveillantes.",
        schema=schema_dict
    )

    return json.loads(reponse_json_str)