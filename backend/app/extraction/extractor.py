import json
from app.llm import get_llm
from app.extraction.schemas import ProfilCV


def extraire_profil_cv(texte_brut: str) -> dict:
    llm = get_llm()

    prompt = f"""
    Voici le texte brut d'un CV. Analyse-le et extrais les informations pour remplir le schéma JSON demandé.
    Si une information n'est pas présente, mets une liste vide ou null.

    Texte du CV :
    {texte_brut}
    """

    # On récupère le schéma JSON de Pydantic
    schema_dict = ProfilCV.model_json_schema()

    # Appel au LLM
    reponse_json_str = llm.generate(
        prompt=prompt,
        system_prompt="Tu es un expert en recrutement. Tu extrais les données des CV de manière stricte.",
        schema=schema_dict
    )

    return json.loads(reponse_json_str)