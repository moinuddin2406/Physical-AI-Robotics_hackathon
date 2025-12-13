"""
RAG (Retrieval-Augmented Generation) service for the textbook
Handles querying the vector database and generating responses with personalization and translation
"""
from typing import List, Dict, Any
import uuid
from sentence_transformers import SentenceTransformer
import numpy as np

from ..models.chapter import QueryRequest, QueryResponse, QueryResult, DocumentChunk, UserPreferences
from ..config.settings import settings
from .content_processor import ContentProcessor
from .translation import MockTranslationService  # Using mock for now


class RAGService:
    """
    Service for handling RAG (Retrieval-Augmented Generation) queries with personalization and translation
    """

    def __init__(self):
        # Initialize the embedding model
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

        # Initialize content processor
        self.content_processor = ContentProcessor()

        # Initialize translation service
        self.translation_service = MockTranslationService()

        # In a real implementation, this would connect to a vector database like Qdrant
        # For this example, we'll store embeddings in memory
        self.chunks: List[DocumentChunk] = []
        self.embeddings: np.ndarray = np.array([])

        # Process all textbook content and generate embeddings
        self._load_content()

    def _load_content(self):
        """
        Load textbook content and generate embeddings
        """
        print("Loading textbook content and generating embeddings...")

        # Process all content into chunks
        self.chunks = self.content_processor.process_all_content()

        # Generate embeddings for all chunks
        chunk_texts = [chunk.content for chunk in self.chunks]
        self.embeddings = self.model.encode(chunk_texts)

        print(f"Loaded {len(self.chunks)} content chunks with embeddings")

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Retrieve the most relevant content chunks for a query
        """
        # Generate embedding for the query
        query_embedding = self.model.encode([query])[0]

        # Calculate similarity between query and all content chunks
        similarities = []
        for i, chunk_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((similarity, i))

        # Sort by similarity and get top-k results
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_similarities = similarities[:top_k]

        # Filter by minimum confidence score
        results = []
        for similarity, idx in top_similarities:
            if similarity >= settings.MIN_CONFIDENCE_SCORE:
                chunk = self.chunks[idx]
                results.append(
                    QueryResult(
                        chunk_id=chunk.id,
                        chapter_id=chunk.chapter_id,
                        content=chunk.content,
                        similarity_score=similarity,
                        metadata=chunk.metadata
                    )
                )

        return results

    def adjust_response_complexity(self, response: str, complexity_level: str) -> str:
        """
        Adjust the complexity of the response based on user preference
        """
        if complexity_level == "beginner":
            # For beginner level, simplify the response
            # This would involve using an LLM to rephrase complex text in simpler terms
            # For now, we'll just add a note
            return f"[BEGINNER LEVEL] {response}"
        elif complexity_level == "advanced":
            # For advanced level, potentially add more technical details
            # This would involve expanding on concepts with more detailed explanations
            # For now, we'll just add a note
            return f"[ADVANCED LEVEL] {response}"
        else:  # intermediate (default)
            return response

    def generate_response(self, query: str, relevant_chunks: List[QueryResult]) -> str:
        """
        Generate a response based on the query and relevant chunks
        """
        if not relevant_chunks:
            return "I couldn't find relevant information in the textbook to answer your question."

        # In a real implementation, this would use an LLM to generate a response
        # For this example, we'll create a simple response based on the first chunk
        response_parts = [
            f"Based on the textbook content, here's what I found regarding your question: '{query}':\n\n"
        ]

        for i, chunk in enumerate(relevant_chunks):
            response_parts.append(f"From {chunk.metadata['source']}:\n{chunk.content}\n")

        response_parts.append("\nThis information is based on the Physical AI & Humanoid Robotics textbook.")

        return " ".join(response_parts)

    def query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a RAG query and return a response with personalization and translation
        """
        # Extract options
        options = query_request.options or {}
        max_chunks = options.get("max_chunks", settings.MAX_RETRIEVAL_CHUNKS)
        response_complexity = options.get("response_complexity", "intermediate")
        language = options.get("language", "en")
        use_personalization = options.get("use_personalization", False)

        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(query_request.query, top_k=max_chunks)

        # Generate response
        response_text = self.generate_response(query_request.query, relevant_chunks)

        # Apply personalization if requested
        if use_personalization:
            response_text = self.adjust_response_complexity(response_text, response_complexity)

        # Apply translation if requested
        if language != "en" and self.translation_service.is_language_supported(language):
            response_text = self.translation_service.translate_text(response_text, language)

        # Determine source chapters
        source_chapters = list(set(chunk.chapter_id for chunk in relevant_chunks))

        # Calculate average confidence
        if relevant_chunks:
            avg_confidence = sum(chunk.similarity_score for chunk in relevant_chunks) / len(relevant_chunks)
        else:
            avg_confidence = 0.0

        # Create and return response
        return QueryResponse(
            response=response_text,
            source_chapters=source_chapters,
            confidence=avg_confidence,
            chunks_used=len(relevant_chunks),
            query_id=str(uuid.uuid4())
        )


# Example usage
if __name__ == "__main__":
    rag_service = RAGService()

    # Example query with options for personalization and translation
    test_query = QueryRequest(
        query="What is Physical AI?",
        options={
            "response_complexity": "beginner",
            "language": "ur",
            "use_personalization": True,
            "max_chunks": 3
        }
    )
    result = rag_service.query(test_query)

    print(f"Query: {test_query.query}")
    print(f"Response: {result.response}")
    print(f"Confidence: {result.confidence}")
    print(f"Source Chapters: {result.source_chapters}")