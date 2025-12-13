# Physical AI & Humanoid Robotics — Essentials

This project implements a comprehensive textbook on Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot that responds exclusively to queries based on the book's content.

## Project Structure

```
my-book/
├── docusaurus.config.js    # Docusaurus configuration
├── package.json            # Node.js dependencies
├── docs/                   # Content directory for textbook chapters
│   ├── intro-physical-ai/      # Chapter 1: Introduction to Physical AI
│   ├── basics-humanoid-robotics/ # Chapter 2: Basics of Humanoid Robotics
│   ├── ros2-fundamentals/      # Chapter 3: ROS 2 Fundamentals
│   ├── digital-twin-simulation/ # Chapter 4: Digital Twin Simulation
│   ├── vision-language-action/  # Chapter 5: Vision-Language-Action Systems
│   └── capstone-pipeline/      # Chapter 6: Capstone: Simple AI-Robot Pipeline
├── src/                    # Custom Docusaurus components
│   ├── components/         # React components
│   ├── pages/              # Additional pages beyond docs
│   └── css/                # Custom styles
├── static/                 # Static assets (images, etc.)
├── backend/                # FastAPI backend for RAG
│   ├── main.py             # FastAPI application entry point
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── api/                # API endpoints
│   └── config/             # Configuration files
├── docker-compose.yml      # Docker services configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker and Docker Compose

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
# Using Docker Compose (recommended)
docker-compose up -d qdrant
```

## Running the Complete Application

### 1. Start All Services
```bash
# Using Docker Compose to start all services
docker-compose up -d
```

### 2. Or Start Services Separately
1. Start Qdrant (vector database): `docker-compose up -d qdrant`
2. Start the FastAPI backend: `uvicorn backend.main:app --reload --port 8000`
3. Start the Docusaurus frontend: `npm start`

### 3. Populate the RAG System
```bash
# Process the textbook content into vector embeddings
cd backend
python -m scripts.process_content
```

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

## Development Commands

### Frontend Commands
```bash
# Build the site for production
npm run build

# Serve the built site locally for testing
npm run serve

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
```

## Key Features

1. **Six Comprehensive Chapters** on Physical AI and Humanoid Robotics
2. **Integrated RAG Chatbot** that responds based only on textbook content
3. **Free-tier Compatible** - All tools work within free service limitations
4. **Bonus Features** - Personalization toggle and potential Urdu translation

## Technologies Used

- **Frontend**: Docusaurus v3
- **Backend**: FastAPI
- **Vector Database**: Qdrant
- **Embeddings**: bge-small-en
- **Language**: Python 3.10+, JavaScript/TypeScript

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request