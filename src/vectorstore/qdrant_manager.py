from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_community.vectorstores import Qdrant
from src.config.settings import Settings
from src.embeddings import get_embeddings
import uuid

class QdrantManager:
    """Manage Qdrant vector store operations"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=Settings.QDRANT_URL,
            api_key=Settings.QDRANT_API_KEY if Settings.QDRANT_API_KEY else None
        )
        self.embeddings = get_embeddings()
        self.collection_name = Settings.COLLECTION_NAME
    
    def create_collection(self, vector_size=768):
        """Create a new collection in Qdrant"""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            print(f"Collection might already exist or error: {e}")
    
    def collection_exists(self):
        """Check if collection exists"""
        try:
            collections = self.client.get_collections()
            return any(c.name == self.collection_name for c in collections.collections)
        except:
            return False
    
    def get_vectorstore(self):
        """Get Langchain Qdrant vectorstore instance"""
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )
    
    def add_documents(self, documents):
        """Add documents to the vector store"""
        try:
            # Method 1: Using Langchain
            vectorstore = self.get_vectorstore()
            vectorstore.add_documents(documents)
            print(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"Error adding documents: {e}")
            print("Trying alternative method...")
            
            # Method 2: Direct Qdrant client (fallback)
            try:
                points = []
                for i, doc in enumerate(documents):
                    # Generate embedding
                    embedding = self.embeddings.embed_query(doc.page_content)
                    
                    # Create point
                    point = PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "page_content": doc.page_content,
                            "metadata": doc.metadata
                        }
                    )
                    points.append(point)
                
                # Upsert points
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                print(f"Added {len(documents)} documents using direct method")
            except Exception as e2:
                print(f"Both methods failed: {e2}")
                raise
    
    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted")
        except Exception as e:
            print(f"Error deleting collection: {e}")