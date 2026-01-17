"""
Script to process textbook content and load it into Qdrant using Google Gemini embeddings
"""
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.rag_service import RAGService


def process_content():
    """
    Process all textbook content, generate Gemini embeddings, and store in Qdrant
    """
    print("Starting content processing with Google Gemini embeddings...")
    print("This will:")
    print("1. Load all textbook content")
    print("2. Generate embeddings using Google Gemini")
    print("3. Store embeddings in Qdrant vector database")

    try:
        # Initialize the RAG service which will handle all processing
        print("\nInitializing RAG service...")
        rag_service = RAGService()

        print("\nContent processing and embedding complete!")
        print(f"Successfully loaded {len(rag_service.chunks)} chunks with embeddings into Qdrant")
        print("The content is now ready for RAG queries.")

    except Exception as e:
        print(f"Error during content processing: {str(e)}")
        print("Make sure GEMINI_API_KEY and QDRANT_URL are properly configured in your environment.")


if __name__ == "__main__":
    process_content()