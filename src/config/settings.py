import os
from dotenv import load_dotenv

load_dotenv()

# Nama Virtual Assistant
BOT_NAME = "Stella"

class Settings:
    """Configuration settings for the chatbot"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
    
    # Qdrant Settings
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "starbucks_docs")
    
    # Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Settings
    TOP_K = int(os.getenv("TOP_K", "6"))
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return True