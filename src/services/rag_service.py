"""
RAG (Retrieval-Augmented Generation) service for the textbook
Handles querying the vector database and generating responses with personalization and translation
"""
from typing import List, Dict, Any
import uuid
import numpy as np
import pickle
from pathlib import Path

from models.chapter import QueryRequest, QueryResponse, QueryResult, DocumentChunk, UserPreferences
from config.settings import settings
from .content_processor import ContentProcessor
from .translation import MockTranslationService  # Using mock for now
from .cohere_service import CohereService
from .qdrant_service import QdrantService


class RAGService:
    """
    Service for handling RAG (Retrieval-Augmented Generation) queries with personalization and translation
    """

    def __init__(self, use_precomputed_embeddings=True):
        # Initialize translation service
        self.translation_service = MockTranslationService()

        # Initialize Qdrant service for vector storage and retrieval
        self.qdrant_service = QdrantService()

        # Initialize Cohere service for embeddings
        # Only initialize if we're not using precomputed embeddings OR if we need it for query processing
        try:
            self.cohere_service = CohereService()
        except Exception as e:
            if "COHERE_API_KEY" in str(e) or "quota" in str(e).lower() or "exceeded" in str(e).lower():
                if not use_precomputed_embeddings:
                    # If we're not using precomputed embeddings, we need the Cohere API key
                    raise e
                else:
                    # If we're using precomputed embeddings, we'll handle the missing key or quota issues gracefully
                    print(f"Warning: Cohere service unavailable: {e}")
                    self.cohere_service = None
            else:
                raise e

        # Initialize Gemini service for text generation (we'll still use Gemini for generation)
        try:
            from .gemini_service import GeminiService
            self.gemini_service = GeminiService()
        except Exception as e:
            print(f"Warning: Gemini service unavailable for text generation: {e}")
            self.gemini_service = None

        if use_precomputed_embeddings:
            # Load precomputed content and embeddings
            self._load_precomputed_content()
        else:
            # Process all textbook content and generate embeddings (for local development)
            self._load_content()

    def _load_precomputed_content(self):
        """
        Load precomputed content chunks and embeddings from files
        """
        print("Loading precomputed content and embeddings...")

        data_dir = Path("data")

        # Check if precomputed files exist
        chunks_path = data_dir / "chunks.pkl"
        embeddings_path = data_dir / "embeddings.pkl"

        if not (chunks_path.exists() and embeddings_path.exists()):
            print("Precomputed files not found. Generating embeddings (this may take a while)...")
            self._load_content()
            return

        # Load precomputed chunks and embeddings
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)

        with open(embeddings_path, 'rb') as f:
            embeddings = pickle.load(f)

        print(f"Loaded {len(self.chunks)} content chunks with embeddings from precomputed files")

        # For Hugging Face Spaces, we'll assume embeddings are already in Qdrant
        # to avoid the long upload process during startup
        print("Content loaded successfully! (Embeddings assumed to be in Qdrant)")

    def _load_content(self):
        """
        Load textbook content and generate embeddings using Cohere, then store in Qdrant
        """
        print("Loading textbook content and generating embeddings...")

        # Initialize content processor
        content_processor = ContentProcessor()

        # Process all content into chunks
        self.chunks = content_processor.process_all_content()

        # Generate embeddings for all chunks using Cohere
        chunk_texts = [chunk.content for chunk in self.chunks]
        print(f"Generating embeddings for {len(chunk_texts)} content chunks...")

        embeddings = self.cohere_service.get_embeddings(chunk_texts)

        # Store chunks and embeddings in Qdrant
        print("Storing chunks and embeddings in Qdrant...")
        self.qdrant_service.store_chunks(self.chunks, embeddings)

        print(f"Loaded {len(self.chunks)} content chunks with embeddings in Qdrant")


    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[QueryResult]:
        """
        Retrieve the most relevant content chunks for a query from Qdrant
        """
        if self.cohere_service is None:
            # Fallback when Cohere API is not available (e.g., due to quota limits)
            # Return some chunks based on simple keyword matching
            print("Cohere service not available, using fallback retrieval method")
            return self._fallback_retrieve_chunks(query, top_k)

        try:
            # Generate embedding for the query using Cohere
            query_embedding = self.cohere_service.get_query_embedding(query)

            # Search in Qdrant for similar chunks
            qdrant_results = self.qdrant_service.search_similar(
                query_embedding=query_embedding,
                top_k=top_k
            )

            # Filter by minimum confidence score and convert to QueryResult objects
            results = []
            for result in qdrant_results:
                if result["similarity_score"] >= settings.MIN_CONFIDENCE_SCORE:
                    results.append(
                        QueryResult(
                            chunk_id=result["chunk_id"],
                            chapter_id=result["chapter_id"],
                            content=result["content"],
                            similarity_score=result["similarity_score"],
                            metadata=result["metadata"]
                        )
                    )

            return results
        except Exception as e:
            # If Cohere API fails (e.g., quota exceeded), use fallback method
            print(f"Cohere API error: {e}. Using fallback retrieval method.")
            return self._fallback_retrieve_chunks(query, top_k)

    def _fallback_retrieve_chunks(self, query: str, top_k: int) -> List[QueryResult]:
        """
        Fallback method to retrieve chunks based on simple keyword matching
        when the Gemini API is not available
        """
        # Simple keyword matching approach
        query_lower = query.lower()
        results = []

        for chunk in self.chunks:
            # Check if query terms appear in the chunk content
            content_lower = chunk.content.lower()
            query_words = query_lower.split()

            # Count matching words
            matches = sum(1 for word in query_words if word in content_lower)

            if matches > 0:  # If at least one word matches
                results.append(
                    QueryResult(
                        chunk_id=chunk.id,
                        chapter_id=chunk.chapter_id,
                        content=chunk.content,
                        similarity_score=matches / len(query_words),  # Simple similarity score
                        metadata=chunk.metadata
                    )
                )

        # Sort by similarity score (descending) and return top_k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]

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
        Generate a response using the available LLM based on the query and relevant chunks
        """
        if not relevant_chunks:
            return "I couldn't find relevant information in the textbook to answer your question."

        # Build context from relevant chunks
        context_parts = ["Here is the relevant information from the textbook to answer your query:"]
        for i, chunk in enumerate(relevant_chunks):
            context_parts.append(f"Section {i+1}: {chunk.content}\n")

        context = "\n".join(context_parts)

        # Create a prompt for the LLM
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Answer the user's question based on the provided context from the textbook.

        Question: {query}

        Context: {context}

        Please provide a comprehensive answer based only on the provided context.
        If the context doesn't contain relevant information to answer the question,
        please state that clearly.
        """

        # Try to generate response using Gemini if available
        if self.gemini_service is not None:
            try:
                response = self.gemini_service.generate_response(prompt)
                return response
            except Exception as e:
                print(f"Gemini API error during response generation: {e}")

        # If Gemini is not available, try Cohere
        if self.cohere_service is not None:
            try:
                response = self.cohere_service.generate_response(prompt)
                return response
            except Exception as e:
                print(f"Cohere API error during response generation: {e}")

        # If neither service is available, return context directly
        print("No LLM service available, returning context directly")
        return f"I found some potentially relevant information, but couldn't generate a detailed response:\n\n{context[:1000]}..."

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

        # For fallback responses, adjust confidence accordingly
        if self.cohere_service is None and self.gemini_service is None:
            avg_confidence = min(avg_confidence, 0.5)  # Lower confidence for fallback responses

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