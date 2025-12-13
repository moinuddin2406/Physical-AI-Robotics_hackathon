"""
Script to process textbook content and load it into the vector database
"""
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.services.content_processor import ContentProcessor
from src.services.rag_service import RAGService


def process_content():
    """
    Process all textbook content and prepare it for the RAG system
    """
    print("Starting content processing...")
    
    # Initialize the content processor
    processor = ContentProcessor()
    
    # Process all content into chunks
    print("Processing textbook content into chunks...")
    chunks = processor.process_all_content()
    
    print(f"Successfully processed {len(chunks)} content chunks")
    
    # Initialize the RAG service which will generate embeddings
    print("Initializing RAG service and generating embeddings...")
    rag_service = RAGService()
    
    print("Content processing complete!")
    print(f"Loaded {len(rag_service.chunks)} chunks with embeddings")
    
    return rag_service


if __name__ == "__main__":
    process_content()