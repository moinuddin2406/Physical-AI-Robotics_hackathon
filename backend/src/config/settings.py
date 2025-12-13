from pydantic import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/textbook"
    
    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en"
    EMBEDDING_DIMENSIONS: int = 384  # for bge-small-en
    
    # API settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # In production, specify actual origins
    
    # RAG settings
    MAX_RETRIEVAL_CHUNKS: int = 5
    MIN_CONFIDENCE_SCORE: float = 0.5
    
    # Content processing settings
    CHUNK_SIZE: int = 512  # tokens
    OVERLAP_SIZE: int = 64  # tokens
    
    class Config:
        env_file = ".env"


settings = Settings()