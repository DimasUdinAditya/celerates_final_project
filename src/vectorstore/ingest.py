from pathlib import Path
from src.utils.pdf_loader import PDFLoader
from src.vectorstore.qdrant_manager import QdrantManager

class DocumentIngestor:
    """Handle document ingestion into vector store"""
    
    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.qdrant_manager = QdrantManager()
    
    def ingest_directory(self, directory_path):
        """Ingest all PDFs from a directory"""
        pdf_dir = Path(directory_path)
        
        if not pdf_dir.exists():
            raise ValueError(f"Directory {directory_path} does not exist")
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return
        
        print(f"Found {len(pdf_files)} PDF files")
        
        all_documents = []
        for pdf_file in pdf_files:
            print(f"Processing {pdf_file.name}...")
            docs = self.pdf_loader.load_and_split(str(pdf_file))
            all_documents.extend(docs)
        
        print(f"Total chunks created: {len(all_documents)}")
        
        if not self.qdrant_manager.collection_exists():
            self.qdrant_manager.create_collection()
        
        self.qdrant_manager.add_documents(all_documents)
        print("Ingestion completed successfully!")
    
    def ingest_file(self, file_path):
        """Ingest a single PDF file"""
        print(f"Processing {file_path}...")
        documents = self.pdf_loader.load_and_split(file_path)
        
        if not self.qdrant_manager.collection_exists():
            self.qdrant_manager.create_collection()
        
        self.qdrant_manager.add_documents(documents)
        print(f"Ingested {len(documents)} chunks from {file_path}")