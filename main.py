import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chapters, rag
from config.settings import settings

# Initialize the RAG service (this will load all content and embeddings)
from services.rag_service import RAGService

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics textbook project, including RAG functionality",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chapters.router, prefix="/api", tags=["chapters"])
app.include_router(rag.router, prefix="/api", tags=["rag"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-13T10:00:00Z"}

# Initialize the RAG service (loading content and embeddings)
# This happens on startup
@app.on_event("startup")
async def startup_event():
    print("Initializing RAG service...")
    app.state.rag_service = RAGService()
    print("RAG service initialized successfully!")

# Make the RAG service available to other modules
# app.state.rag_service is set in the startup_event

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)