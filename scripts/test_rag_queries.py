"""
Simple test script to validate the RAG functionality with Gemini and Qdrant
"""
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.chapter import QueryRequest
from src.services.rag_service import RAGService


def test_rag_functionality():
    """
    Test the RAG functionality with sample queries
    """
    print("Initializing RAG service for testing...")
    print("This will load all textbook content and generate embeddings using Gemini...")
    print("Then store embeddings in Qdrant for fast retrieval...")

    try:
        rag_service = RAGService()
        print("RAG service initialized successfully!")
    except Exception as e:
        print(f"Error initializing RAG service: {str(e)}")
        print("Make sure GEMINI_API_KEY and QDRANT_URL are properly configured in your environment.")
        return

    # Define test queries
    test_queries = [
        "What is Physical AI?",
        "Explain ROS 2 fundamentals",
        "How do humanoid robots maintain balance?",
        "What is a digital twin in robotics?",
        "Describe Vision-Language-Action systems"
    ]

    print("\nTesting RAG functionality with sample queries:\n")

    for i, query_text in enumerate(test_queries, 1):
        print(f"Test {i}: Query: '{query_text}'")

        # Create a query request
        query_request = QueryRequest(query=query_text)

        # Process the query
        try:
            response = rag_service.query(query_request)

            print(f"  Response preview: {response.response[:200]}...")
            print(f"  Confidence: {response.confidence:.2f}")
            print(f"  Source chapters: {response.source_chapters}")
            print(f"  Chunks used: {response.chunks_used}")
            print()

        except Exception as e:
            print(f"  Error processing query: {str(e)}")
            print()


if __name__ == "__main__":
    test_rag_functionality()