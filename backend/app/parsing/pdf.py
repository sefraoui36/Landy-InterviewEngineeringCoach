import pymupdf as fitz
import os

def parse_pdf(file_path: str)->str:
    """
    Lit un fichier PDF et retourne son contenu sous forme de texte brut
    """
    if not os.path.exists(file_path):
         raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    text = ""
    try:
        # Ouvrir le document
        doc = fitz.open(file_path)

        # Extraire le texte page par page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text") + "\n"

        doc.close()
        return text.strip()

    except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture du PDF : {str(e)}")

