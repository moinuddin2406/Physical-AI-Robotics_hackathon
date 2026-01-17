import os
from pathlib import Path
import sys

# Add the project root directory to Python path to handle package imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add the backend/src directory to the Python path so imports work correctly
backend_dir = project_root / "backend"
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

# Set environment variable to use precomputed embeddings
os.environ.setdefault("USE_PRECOMPUTED_EMBEDDINGS", "true")

# Set PYTHONPATH environment variable for subprocess calls
current_pythonpath = os.environ.get('PYTHONPATH', '')
new_paths = [str(src_dir), str(backend_dir)]
if current_pythonpath:
    new_paths.append(current_pythonpath)
os.environ['PYTHONPATH'] = os.pathsep.join(new_paths)

# Import and expose the FastAPI app
from backend.src.api import chapters, rag
from backend.src.config.settings import settings
from backend.src.services.rag_service import RAGService

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics textbook project, including RAG functionality with Cohere and Qdrant",
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
    print("Initializing RAG service with Cohere and Qdrant...")
    try:
        # Use precomputed embeddings in production environments (like Hugging Face Spaces)
        use_precomputed = os.getenv("USE_PRECOMPUTED_EMBEDDINGS", "true").lower() == "true"
        app.state.rag_service = RAGService(use_precomputed_embeddings=use_precomputed)
        print("RAG service with Cohere and Qdrant initialized successfully!")
    except Exception as e:
        print(f"Error initializing RAG service: {e}")
        # Create a minimal service that can handle requests with fallback responses
        from backend.src.services.rag_service import RAGService
        # Even if initialization fails, we'll try to create a service that uses fallback methods
        app.state.rag_service = RAGService(use_precomputed_embeddings=True)
        print("RAG service initialized with fallback methods due to error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 7860)))