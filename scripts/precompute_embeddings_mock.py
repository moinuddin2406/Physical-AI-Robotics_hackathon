"""
Script to pre-compute embeddings and save them for faster loading
For Hugging Face Spaces, we'll simulate embeddings since we can't call the Gemini API during deployment
"""
import pickle
import json
from pathlib import Path
import sys
import numpy as np

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add the src directory to the Python path
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from src.services.content_processor import ContentProcessor
from src.config.settings import settings


def precompute_and_save_embeddings():
    print("Loading content...")
    content_processor = ContentProcessor()
    chunks = content_processor.process_all_content()
    print(f"Loaded {len(chunks)} content chunks")

    print("Simulating embeddings generation (using random vectors)...")
    # Simulate embeddings using random vectors of the correct dimension
    embeddings = [np.random.random(settings.EMBEDDING_DIMENSIONS).tolist() for _ in range(len(chunks))]
    
    print(f"Simulated {len(embeddings)} embeddings")

    # Save chunks and embeddings
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save chunks
    with open(data_dir / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    # Save embeddings
    with open(data_dir / "embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)
    
    print(f"Saved {len(chunks)} chunks and {len(embeddings)} simulated embeddings to data/ directory")
    
    # Note: We won't store in Qdrant here since that requires the real service running


if __name__ == "__main__":
    precompute_and_save_embeddings()