"""
Qdrant vector database service for RAG system
"""
from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from config.settings import settings
from models.chapter import DocumentChunk


class QdrantService:
    """
    Service for handling vector database operations with Qdrant
    """
    
    def __init__(self):
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=False
            )
            self.collection_name = "textbook_chunks"
            self._init_collection()
        except Exception as e:
            print(f"Warning: Could not connect to Qdrant: {e}")
            # In case of connection failure, we'll set client to None
            # and handle it gracefully in other methods
            self.client = None
            self.collection_name = "textbook_chunks"
    
    def _init_collection(self):
        """
        Initialize the collection in Qdrant if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except:
            try:
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=settings.EMBEDDING_DIMENSIONS,  # Gemini embedding dimensions
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Created collection '{self.collection_name}'")
            except Exception as e:
                # Handle the case where collection already exists
                if "already exists" in str(e):
                    print(f"Collection '{self.collection_name}' already exists")
                else:
                    raise e
    
    def store_chunks(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):
        """
        Store document chunks and their embeddings in Qdrant
        """
        if self.client is None:
            print("Warning: Qdrant client not available, skipping store_chunks operation")
            return

        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.id)),  # Consistent ID generation
                vector=embedding,
                payload={
                    "chunk_id": chunk.id,
                    "chapter_id": chunk.chapter_id,
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata
                }
            )
            points.append(point)

        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks based on query embedding
        """
        if self.client is None:
            print("Warning: Qdrant client not available, returning empty search results")
            return []

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results to match our expected structure
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "chunk_id": result.payload["chunk_id"],
                "chapter_id": result.payload["chapter_id"],
                "content": result.payload["content"],
                "similarity_score": result.score,
                "metadata": result.payload["metadata"]
            })

        return formatted_results
    
    def clear_collection(self):
        """
        Clear all vectors from the collection
        """
        self.client.delete_collection(self.collection_name)
        self._init_collection()