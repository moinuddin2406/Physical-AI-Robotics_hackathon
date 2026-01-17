# Backend Architecture - Migrated to Google Gemini

## Overview
This project has been migrated from OpenAI to Google Gemini API for both embeddings and text generation. The architecture now uses:

- **Google Gemini** for text embeddings and generation
- **Qdrant** as the vector database for efficient similarity search
- **FastAPI** as the web framework

## Key Changes

### 1. Embeddings
- Previously used SentenceTransformer for embeddings
- Now uses Google's `models/embedding-001` model via Gemini API
- Implemented in `src/services/gemini_service.py`

### 2. Text Generation
- Previously used placeholder response generation
- Now uses Google's `gemini-1.5-flash` model for response generation
- Implemented in `src/services/gemini_service.py`

### 3. Vector Storage
- Previously stored embeddings in memory
- Now uses Qdrant vector database for persistence and efficient retrieval
- Implemented in `src/services/qdrant_service.py`

### 4. RAG Flow
- Content is processed through `content_processor.py`
- Embeddings are generated using Gemini embeddings
- Chunks and embeddings are stored in Qdrant
- Query embeddings are generated and searched in Qdrant
- Context from relevant chunks is sent to Gemini LLM for response generation

## Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your-gemini-api-key-here
QDRANT_URL=http://localhost:6333
# Optional: QDRANT_API_KEY=your-qdrant-api-key-if-using-cloud
ALLOWED_ORIGINS=["*"]
```

### Dependencies
- `google-generativeai`: For Gemini API integration
- `qdrant-client`: For vector database operations
- Removed `sentence-transformers` dependency

## Services

### GeminiService (`src/services/gemini_service.py`)
Handles both embeddings and text generation using Google Gemini:

- `get_embeddings()`: Generate embeddings for multiple texts
- `get_query_embedding()`: Generate embeddings for a single query
- `generate_response()`: Generate responses using Gemini LLM

### QdrantService (`src/services/qdrant_service.py`)
Manages vector storage and retrieval:

- `store_chunks()`: Store document chunks with embeddings
- `search_similar()`: Find similar chunks to a query
- `clear_collection()`: Clear all stored vectors

### RAGService (`src/services/rag_service.py`)
Integrates all components for RAG functionality:

- Loads textbook content and generates embeddings
- Stores embeddings in Qdrant
- Retrieves relevant information for queries
- Generates responses using Gemini
- Handles personalization and translation

## Usage

1. Set up Qdrant (local or cloud)
2. Get a Google Gemini API key
3. Configure environment variables
4. Run the application
5. Content will be processed and embeddings stored in Qdrant on startup
6. Query the `/api/query` endpoint to get responses

## API Endpoints

- `GET /health`: Health check
- `GET /api/chapters`: List all chapters
- `GET /api/chapters/{chapter_id}`: Get specific chapter details  
- `POST /api/query`: Submit a query to the RAG system

## Testing

Use the test script to verify functionality:

```bash
python scripts/test_rag_queries.py
```