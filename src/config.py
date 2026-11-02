"""
Configuración centralizada del asistente RAG.
Lee variables de entorno desde .env (o del sistema en producción).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ------------- Groq (LLM provider A) -------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

# ------------- Google Gemini (LLM provider B) -------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ------------- Parámetros LLM compartidos -------------
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "600"))

# Provider por defecto al arrancar la app ("groq" o "gemini")
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "groq")

# ------------- Embeddings -------------
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)

# ------------- Chunking -------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# ------------- Retrieval -------------
TOP_K = int(os.getenv("TOP_K", "5"))

# ------------- Storage -------------
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./vectorstore/index.pkl")
DOCS_PATH = os.getenv("DOCS_PATH", "./documentos")
