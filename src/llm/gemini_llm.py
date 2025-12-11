from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import Settings

def get_llm(temperature: float | None = None):
    """Initialize and return Gemini LLM"""
    Settings.validate()
    
    if temperature is None:
        temperature = Settings.LLM_TEMPERATURE

    llm = ChatGoogleGenerativeAI(
        model=Settings.MODEL_NAME,
        google_api_key=Settings.GEMINI_API_KEY,
        temperature=temperature,
        convert_system_message_to_human=True
    )
    
    return llm