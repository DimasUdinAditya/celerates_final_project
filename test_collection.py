import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.vectorstore.qdrant_manager import QdrantManager

def main():
    print("Checking Qdrant collection...")
    
    manager = QdrantManager()
    
    # Cek apakah collection ada
    exists = manager.collection_exists()
    print(f"Collection '{manager.collection_name}' exists: {exists}")
    
    if exists:
        # Cek info collection
        try:
            collection_info = manager.client.get_collection(manager.collection_name)
            print(f"\nCollection Info:")
            print(f"  Points count: {collection_info.points_count}")
            print(f"  Vectors count: {collection_info.vectors_count}")
            print(f"  Status: {collection_info.status}")
        except Exception as e:
            print(f"Error getting collection info: {e}")
    else:
        print("\n❌ Collection does not exist!")
        print("Run: python scripts/setup_vectorstore.py")

if __name__ == "__main__":
    main()