"""
Script to precompute embeddings using Cohere for Hugging Face deployment
This script generates embeddings for all textbook content and saves them to files
so they can be loaded quickly during Hugging Face Space startup.
"""
import os
import pickle
from pathlib import Path
import sys

# Add the backend/src directory to the Python path
project_root = Path(__file__).parent.parent.parent
src_dir = project_root / "backend" / "src"
sys.path.insert(0, str(src_dir))

from src.services.content_processor import ContentProcessor
from src.services.cohere_service import CohereService


def main():
    print("Precomputing embeddings using Cohere...")
    
    # Create data directory if it doesn't exist
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Initialize services
    content_processor = ContentProcessor()
    cohere_service = CohereService()
    
    # Process all content into chunks
    print("Processing textbook content into chunks...")
    chunks = content_processor.process_all_content()
    print(f"Processed {len(chunks)} content chunks")
    
    # Extract text content from chunks
    chunk_texts = [chunk.content for chunk in chunks]
    
    # Generate embeddings using Cohere
    print("Generating embeddings using Cohere...")
    embeddings = cohere_service.get_embeddings(chunk_texts)
    print(f"Generated embeddings for {len(embeddings)} chunks")
    
    # Save chunks and embeddings to files
    chunks_path = data_dir / "chunks.pkl"
    embeddings_path = data_dir / "embeddings.pkl"
    
    print(f"Saving chunks to {chunks_path}...")
    with open(chunks_path, 'wb') as f:
        pickle.dump(chunks, f)
    
    print(f"Saving embeddings to {embeddings_path}...")
    with open(embeddings_path, 'wb') as f:
        pickle.dump(embeddings, f)
    
    print("Precomputation complete!")
    print(f"Saved {len(chunks)} chunks and {len(embeddings)} embeddings to:")
    print(f"  - {chunks_path}")
    print(f"  - {embeddings_path}")


if __name__ == "__main__":
    main()