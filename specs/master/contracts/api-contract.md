# API Contract: Physical AI & Humanoid Robotics — Essentials

## Overview
This document defines the API contracts for the RAG system integrated with the Physical AI & Humanoid Robotics textbook.

## Base URL
`https://api.my-book.example.com` (production)
`http://localhost:8000` (development)

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Authentication
None required for basic functionality (free-tier constraint).
Future extension could include API keys if needed.

## API Endpoints

### 1. Health Check
#### GET /health
Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-13T10:00:00Z"
}
```

### 2. RAG Query
#### POST /api/query
Submit a query to the RAG system and receive a response based on textbook content.

**Request:**
```json
{
  "query": "What is ROS 2?",
  "options": {
    "response_complexity": "beginner",
    "language": "en",
    "use_personalization": true,
    "max_chunks": 5
  }
}
```

**Parameters:**
- `query`: (string, required) The user's question
- `options`: (object, optional) Additional options for the query
  - `response_complexity`: (string) "beginner", "intermediate", or "advanced" (default: "intermediate")
  - `language`: (string) Language code (default: "en")
  - `use_personalization`: (boolean) Whether to apply personalization (default: false)
  - `max_chunks`: (integer) Maximum number of content chunks to consider (default: 3, max: 10)

**Success Response (200):**
```json
{
  "response": "ROS 2 (Robot Operating System 2) is a flexible framework for...",
  "source_chapters": ["ros2-fundamentals"],
  "confidence": 0.85,
  "chunks_used": 3,
  "query_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid query parameters",
  "details": "Query must be at least 5 characters long"
}
```

**Error Response (500):**
```json
{
  "error": "Internal server error",
  "details": "An unexpected error occurred processing your request"
}
```

### 3. List Chapters
#### GET /api/chapters
Get a list of all available textbook chapters.

**Response:**
```json
{
  "chapters": [
    {
      "id": "intro-physical-ai",
      "title": "Introduction to Physical AI",
      "description": "Definition and scope of Physical AI",
      "word_count": 1200,
      "position": 1
    },
    {
      "id": "basics-humanoid-robotics",
      "title": "Basics of Humanoid Robotics",
      "description": "Anatomy and design principles",
      "word_count": 1450,
      "position": 2
    },
    {
      "id": "ros2-fundamentals",
      "title": "ROS 2 Fundamentals",
      "description": "ROS 2 architecture and concepts",
      "word_count": 1380,
      "position": 3
    },
    {
      "id": "digital-twin-simulation",
      "title": "Digital Twin Simulation",
      "description": "Gazebo simulation environment",
      "word_count": 1320,
      "position": 4
    },
    {
      "id": "vision-language-action",
      "title": "Vision-Language-Action Systems",
      "description": "Perception systems and multi-modal learning",
      "word_count": 1410,
      "position": 5
    },
    {
      "id": "capstone-pipeline",
      "title": "Capstone: Simple AI-Robot Pipeline",
      "description": "Integration of concepts from previous chapters",
      "word_count": 1500,
      "position": 6
    }
  ]
}
```

### 4. Get Chapter Details
#### GET /api/chapters/{chapter_id}
Get detailed information about a specific chapter.

**Parameters:**
- `chapter_id`: (string, required) The ID of the chapter to retrieve

**Response:**
```json
{
  "id": "ros2-fundamentals",
  "title": "ROS 2 Fundamentals",
  "content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) is a flexible framework...",
  "word_count": 1380,
  "learning_objectives": [
    "Understand the architecture of ROS 2",
    "Learn about nodes, topics, services, and actions",
    "Practice with package management in ROS 2"
  ],
  "key_concepts": [
    "Nodes",
    "Topics",
    "Services",
    "Actions",
    "Packages"
  ],
  "prerequisites": [
    "intro-physical-ai",
    "basics-humanoid-robotics"
  ],
  "related_chapters": [
    "digital-twin-simulation",
    "vision-language-action"
  ]
}
```

### 5. Get Chapter Exercises
#### GET /api/chapters/{chapter_id}/exercises
Get exercises for a specific chapter.

**Parameters:**
- `chapter_id`: (string, required) The ID of the chapter

**Response:**
```json
{
  "chapter_id": "ros2-fundamentals",
  "exercises": [
    {
      "id": "ros2-fundamentals-ex1",
      "type": "multiple_choice",
      "question": "What is a ROS 2 node?",
      "options": [
        "A physical robot component",
        "A network of computers",
        "A process that performs computation",
        "A type of sensor"
      ],
      "answer": "A process that performs computation",
      "explanation": "In ROS 2, a node is a process that performs computation. Nodes are the fundamental building blocks of ROS applications.",
      "difficulty": "beginner"
    },
    {
      "id": "ros2-fundamentals-ex2",
      "type": "short_answer",
      "question": "Explain the difference between a topic and a service in ROS 2.",
      "answer": "Topics provide one-way, asynchronous communication using a publish-subscribe pattern, while services provide two-way, synchronous communication using a request-response pattern.",
      "difficulty": "intermediate"
    }
  ]
}
```

### 6. Submit Exercise Answer
#### POST /api/exercises/{exercise_id}/submit
Submit an answer to an exercise and get feedback.

**Request:**
```json
{
  "answer": "A process that performs computation",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "exercise_id": "ros2-fundamentals-ex1",
  "is_correct": true,
  "feedback": "Correct! A ROS 2 node is indeed a process that performs computation.",
  "explanation": "In ROS 2, a node is a process that performs computation. Nodes are the fundamental building blocks of ROS applications."
}
```

## Error Codes
- `200`: Success
- `400`: Bad Request - Invalid input parameters
- `404`: Not Found - Resource does not exist
- `500`: Internal Server Error - An unexpected error occurred

## Rate Limiting
- API is limited to 100 requests per hour per IP address (free-tier constraint)
- Exceeding the limit results in a 429 (Too Many Requests) response

## Response Time Expectations
- Health check: < 100ms
- List chapters: < 200ms
- Get chapter details: < 300ms
- RAG query: < 3000ms (depending on complexity)