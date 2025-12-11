import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vectorstore.ingest import DocumentIngestor

def main():
    """Ingest documents from data/raw directory"""
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    if not data_dir.exists():
        print(f"❌ Directory {data_dir} does not exist!")
        print("Please create the directory and add PDF files:")
        print(f"   mkdir {data_dir}")
        return
    
    pdf_files = list(data_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDF files found in {data_dir}")
        print("Please add PDF files to the directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    print(f"\nIngesting documents from: {data_dir}")
    
    ingestor = DocumentIngestor()
    ingestor.ingest_directory(str(data_dir))

if __name__ == "__main__":
    main()