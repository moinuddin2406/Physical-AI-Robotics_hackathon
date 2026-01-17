"""
Script to pre-compute embeddings and save them for faster loading
"""
import pickle
import json
from pathlib import Path
import sys

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add the src directory to the Python path
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from src.services.content_processor import ContentProcessor
from src.services.gemini_service import GeminiService
from src.services.qdrant_service import QdrantService
from src.models.chapter import DocumentChunk


def precompute_and_save_embeddings():
    print("Loading content...")
    content_processor = ContentProcessor()
    chunks = content_processor.process_all_content()
    print(f"Loaded {len(chunks)} content chunks")

    print("Generating embeddings...")
    gemini_service = GeminiService()
    chunk_texts = [chunk.content for chunk in chunks]
    
    # Generate embeddings in batches to avoid rate limits
    embeddings = []
    batch_size = 10  # Small batch to avoid rate limits
    
    for i in range(0, len(chunk_texts), batch_size):
        batch_texts = chunk_texts[i:i+batch_size]
        batch_embeddings = gemini_service.get_embeddings(batch_texts)
        embeddings.extend(batch_embeddings)
        print(f"Processed batch {i//batch_size + 1}/{(len(chunk_texts) - 1)//batch_size + 1}")
    
    print(f"Generated {len(embeddings)} embeddings")

    # Save chunks and embeddings
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save chunks
    with open(data_dir / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    # Save embeddings
    with open(data_dir / "embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)
    
    print(f"Saved {len(chunks)} chunks and {len(embeddings)} embeddings to data/ directory")
    
    # Also store in Qdrant
    print("Storing in Qdrant...")
    qdrant_service = QdrantService()
    qdrant_service.store_chunks(chunks, embeddings)
    print("Stored in Qdrant successfully")


if __name__ == "__main__":
    precompute_and_save_embeddings()