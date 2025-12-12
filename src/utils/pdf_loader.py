from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from src.config.settings import Settings

class PDFLoader:
    """Load and process PDF documents"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Settings.CHUNK_SIZE,
            chunk_overlap=Settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path):
        """Load a PDF file"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    def split_documents(self, documents):
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def load_and_split(self, file_path):
        """Load PDF and split into chunks"""
        documents = self.load_pdf(file_path)
        chunks = self.split_documents(documents)
        return chunks
