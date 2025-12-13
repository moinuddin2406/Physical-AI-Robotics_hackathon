# Quickstart Guide: Physical AI & Humanoid Robotics — Essentials

## Overview
This guide provides a quick start to the development environment and core functionality for the Physical AI & Humanoid Robotics textbook project.

## Prerequisites
- Node.js 18+ (for Docusaurus frontend)
- Python 3.10+ (for FastAPI backend)
- Git (for version control)
- npm or yarn (Node.js package managers)

## Setting Up the Development Environment

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/my-book.git
cd my-book
```

### 2. Set Up the Frontend (Docusaurus)
```bash
# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The site will be accessible at `http://localhost:3000`.

### 3. Set Up the Backend (FastAPI)
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --reload --port 8000
```

The API will be accessible at `http://localhost:8000`.

### 4. Set Up Qdrant Vector Database
```bash
# Option 1: Using Docker
docker run -p 6333:6333 --name qdrant-container qdrant/qdrant

# Option 2: Install locally (if Docker not available)
# Follow installation instructions at: https://qdrant.tech/documentation/guides/installation/
```

## Running the Complete Application

### 1. Start the Services
1. Start Qdrant (vector database)
2. Start the FastAPI backend: `uvicorn backend.main:app --reload --port 8000`
3. Start the Docusaurus frontend: `npm start`

### 2. Populate the RAG System
```bash
# Process the textbook content into vector embeddings
cd backend
python -m scripts.process_content
```

### 3. Using the RAG Chatbot
1. Navigate to the textbook site (frontend)
2. Find the chatbot interface, typically in the sidebar or at the bottom of each chapter
3. Ask questions related to the textbook content
4. The chatbot will retrieve relevant sections and generate a response

## Key Development Commands

### Frontend Commands
```bash
# Build the site for production
npm run build

# Serve the built site locally for testing
npm run serve

# Run tests
npm test

# Deploy to GitHub Pages
npm run deploy
```

### Backend Commands
```bash
# Run backend tests
python -m pytest tests/

# Run the backend with auto-reload
uvicorn backend.main:app --reload

# Process content and update vector database
python -m scripts.process_content

# Run RAG query tests
python -m scripts.test_rag_queries
```

## Adding New Content

### 1. Create a New Chapter
1. Create a new directory in the `docs/` folder
2. Add a `README.md` file with the chapter content
3. Update `sidebars.js` to include the new chapter in the navigation

### 2. Update the RAG System
After adding new content:
1. Run the content processing script: `python -m scripts.process_content`
2. The new content will be chunked and added to the vector database

## Configuration Files

### Docusaurus Configuration (`docusaurus.config.js`)
- Site title, description, and meta information
- Theme configuration
- Plugin settings
- Deployment settings for GitHub Pages

### Backend Configuration (`backend/config/settings.py`)
- Database connection settings
- Embedding model configuration
- API rate limits
- CORS settings

## API Endpoints

### RAG Query Endpoint
- **POST** `/api/query`
- Request: `{ "query": "your question here", "options": {...} }`
- Response: `{ "response": "answer", "source_chapters": [...], "confidence": 0.85 }`

### Health Check Endpoint
- **GET** `/health`
- Response: `{ "status": "healthy" }`

### Content Endpoints
- **GET** `/api/chapters` - List all chapters
- **GET** `/api/chapters/:id` - Get a specific chapter

## Bonus Features

### Personalization Toggle
1. Toggle available in the UI
2. Adjusts response complexity based on user preference
3. Configured via query options: `{ "response_complexity": "beginner" }`

### Urdu Translation Mode
1. Available as a language toggle in the UI
2. Translates responses to Urdu when enabled
3. Configured via query options: `{ "language": "ur" }`

## Troubleshooting

### Common Issues

**Frontend won't start:**
- Ensure Node.js and npm are properly installed
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Backend can't connect to Qdrant:**
- Check that Qdrant is running and accessible
- Verify connection settings in `backend/config/settings.py`
- Ensure the Qdrant collection exists

**RAG queries return no results:**
- Verify that content has been processed and loaded into the vector database
- Check that the embedding model is correctly configured
- Verify query processing is working

### Development Tips

1. **Efficient Development:**
   - Use `npm start` for frontend development with hot reloading
   - Use `uvicorn --reload` for backend development with auto-restart

2. **Testing RAG Functionality:**
   - Use short sample queries during development
   - Monitor confidence scores to ensure quality responses

3. **Performance Optimization:**
   - Limit the number of chunks retrieved in development
   - Use smaller embedding models for faster processing during development

## Deployment

### Frontend to GitHub Pages
1. Ensure GitHub repository is configured properly
2. Run: `npm run deploy`
3. GitHub Pages will automatically deploy from the `gh-pages` branch

### Backend to Fly.io
1. Install Fly CLI: `flyctl auth login`
2. Configure the app: `flyctl launch`
3. Deploy: `flyctl deploy`

For detailed deployment instructions, refer to the deployment documentation in the `docs/deployment/` directory.