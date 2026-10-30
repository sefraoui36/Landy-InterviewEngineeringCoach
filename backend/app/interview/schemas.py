from pydantic import BaseModel,Field
from typing import List
class Question(BaseModel):
    texte: str= Field(description="La question posé par le recruteur ")
    competence_ciblee: str= Field(description="La compétence ou le projet ciblé par le question ")
    type_question: str=Field(description="Type de question : 'projet','technique', 'comportementale', 'motivation'")
    but: str = Field(description="Ce que le recruteur cherche à évaluer avec cette question")

class PlanEntretien(BaseModel):
    questions: List[Question] = Field(description="La liste ordonnée des questions de l'entretien")