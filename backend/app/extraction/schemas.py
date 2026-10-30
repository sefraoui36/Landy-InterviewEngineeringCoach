from pydantic import BaseModel, Field
from typing import List, Optional

class Competence(BaseModel):
    nom: str = Field(description="Le nom de la compétence (ex: Python, React, Gestion de projet)")
    niveau: str = Field(description="Niveau estimé : 'utilisé en projet' ou 'connu en théorie'")

class Projet(BaseModel):
    nom: str = Field(description="Le nom du projet")
    description: str = Field(description="Une courte description de ce qui a été fait")
    technologies: List[str] = Field(description="Les technologies utilisées dans ce projet")

class ProfilCV(BaseModel):
    nom: str = Field(description="Prénom et Nom du candidat")
    titre: Optional[str] = Field(description="Titre professionnel (ex: Ingénieur Logiciel, Data Scientist)")
    experiences: List[str] = Field(description="Liste des expériences professionnelles avec entreprise et dates")
    competences: List[Competence] = Field(description="Liste des compétences extraites du CV")
    projets: List[Projet] = Field(description="Liste des projets présentés dans le CV")