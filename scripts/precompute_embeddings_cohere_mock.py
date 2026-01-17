"""
Mock script to precompute embeddings using random vectors for Hugging Face deployment testing
This script generates mock embeddings for all textbook content and saves them to files
so they can be loaded during Hugging Face Space startup when no Cohere API key is available.
"""
import os
import pickle
import numpy as np
from pathlib import Path
import sys

# Add the backend/src directory to the Python path
project_root = Path(__file__).parent.parent.parent
src_dir = project_root / "backend" / "src"
sys.path.insert(0, str(src_dir))

from src.services.content_processor import ContentProcessor
from src.config.settings import settings


def main():
    print("Precomputing MOCK embeddings for testing...")
    
    # Create data directory if it doesn't exist
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Initialize content processor
    content_processor = ContentProcessor()
    
    # Process all content into chunks
    print("Processing textbook content into chunks...")
    chunks = content_processor.process_all_content()
    print(f"Processed {len(chunks)} content chunks")
    
    # Generate mock embeddings (random vectors with proper dimensions)
    print(f"Generating {settings.EMBEDDING_DIMENSIONS}-dimensional mock embeddings...")
    embeddings = []
    for i in range(len(chunks)):
        # Generate random embedding vector with proper dimensions
        mock_embedding = np.random.rand(settings.EMBEDDING_DIMENSIONS).astype(np.float32).tolist()
        embeddings.append(mock_embedding)
    
    print(f"Generated mock embeddings for {len(embeddings)} chunks")
    
    # Save chunks and embeddings to files
    chunks_path = data_dir / "chunks.pkl"
    embeddings_path = data_dir / "embeddings.pkl"
    
    print(f"Saving chunks to {chunks_path}...")
    with open(chunks_path, 'wb') as f:
        pickle.dump(chunks, f)
    
    print(f"Saving embeddings to {embeddings_path}...")
    with open(embeddings_path, 'wb') as f:
        pickle.dump(embeddings, f)
    
    print("Mock precomputation complete!")
    print(f"Saved {len(chunks)} chunks and {len(embeddings)} embeddings to:")
    print(f"  - {chunks_path}")
    print(f"  - {embeddings_path}")
    print("\nNote: These are mock embeddings for testing purposes only.")


if __name__ == "__main__":
    main()