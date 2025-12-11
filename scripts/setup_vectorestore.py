import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vectorstore.qdrant_manager import QdrantManager

def main():
    """Setup Qdrant vector store"""
    print("Setting up Qdrant vector store...")
    
    manager = QdrantManager()
    
    if manager.collection_exists():
        print(f"Collection '{manager.collection_name}' already exists")
        response = input("Do you want to delete and recreate? (yes/no): ")
        if response.lower() == 'yes':
            manager.delete_collection()
            manager.create_collection()
    else:
        manager.create_collection()
    
    print("Setup completed!")

if __name__ == "__main__":
    main()