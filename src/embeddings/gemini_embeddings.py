from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.settings import Settings

def get_embeddings():
    """Initialize and return Gemini embeddings model"""
    Settings.validate()
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model=Settings.EMBEDDING_MODEL,
        google_api_key=Settings.GEMINI_API_KEY
    )
    
    return embeddings