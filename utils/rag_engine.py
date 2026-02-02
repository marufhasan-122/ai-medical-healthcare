import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
logger = logging.getLogger(__name__)

class MedicalRAG:
    def __init__(self, vector_path="vector_store/medical"):
        if not os.path.exists(vector_path):
            raise FileNotFoundError(f"Vector store not found at {vector_path}. Run ingest_pdfs.py first.")
        
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
            self.vector_path = vector_path
            # Load without the allow_dangerous_deserialization parameter for compatibility
            self.db = FAISS.load_local(vector_path, self.embeddings)
            logger.info(f"MedicalRAG initialized with vector store at {vector_path}")
        except Exception as e:
            logger.error(f"Failed to initialize MedicalRAG: {e}")
            raise

    def retrieve(self, query, k=3):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        # Input validation
        if len(query) > 5000:
            raise ValueError("Query exceeds maximum length of 5000 characters")
        
        try:
            docs = self.db.similarity_search(query, k=k)
            if not docs:
                logger.warning(f"No documents found for query: {query[:100]}...")
                return "No relevant medical information found."
            return "\n".join([d.page_content for d in docs])
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            raise RuntimeError(f"Failed to retrieve documents: {e}")
