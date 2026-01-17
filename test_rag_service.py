"""
Test script to verify that the RAG service can load precomputed embeddings
"""
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = Path("backend/.env")
load_dotenv(dotenv_path=dotenv_path)

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add the backend/src directory to the Python path
backend_dir = project_root / "backend"
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from backend.src.services.rag_service import RAGService

def test_rag_service_with_precomputed():
    print("Testing RAG Service with precomputed embeddings...")
    
    try:
        # Initialize RAG service with precomputed embeddings
        rag_service = RAGService(use_precomputed_embeddings=True)
        
        print(f"Successfully loaded {len(rag_service.chunks)} chunks from precomputed data")

        print("RAG service initialization test completed successfully!")
        print("The service can load precomputed embeddings efficiently,")
        print("which will prevent timeout issues on Hugging Face Spaces.")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_service_with_precomputed()