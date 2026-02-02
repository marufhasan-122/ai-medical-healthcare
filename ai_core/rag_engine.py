import os
from langchain_community.document_loaders import PyPDFLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "knowledge_base.pdf")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"Knowledge base not found at {PDF_PATH}")

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()