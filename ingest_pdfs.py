from utils.pdf_loader import load_and_split_pdf
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Support both single PDF and directory of PDFs
pdf_file = "knowledge_base.pdf"
pdf_dir = "knowledge_base"

all_docs = []

# Check if single PDF exists
if os.path.exists(pdf_file):
    print(f"Loading {pdf_file}...")
    all_docs.extend(load_and_split_pdf(pdf_file))
# Otherwise check for directory
elif os.path.exists(pdf_dir):
    print(f"Loading PDFs from {pdf_dir} directory...")
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            print(f"  Loading {file}...")
            all_docs.extend(load_and_split_pdf(os.path.join(pdf_dir, file)))
else:
    raise FileNotFoundError(f"Neither {pdf_file} nor {pdf_dir} directory found")

if not all_docs:
    raise ValueError("No documents were loaded. Check your PDF files.")

print(f"\\nLoaded {len(all_docs)} document chunks")
print("Creating embeddings and vector store...")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(all_docs, embeddings)

# Ensure output directory exists
os.makedirs("vector_store", exist_ok=True)
db.save_local("vector_store/medical")

print("✅ Medical PDFs indexed")
