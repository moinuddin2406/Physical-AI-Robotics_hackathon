# Data Model: Physical AI & Humanoid Robotics — Essentials

## Overview
This document defines the data models for the Physical AI & Humanoid Robotics textbook project, including content structure, metadata, and RAG system data requirements.

## Content Structure

### Chapter Entity
- **id**: String (unique identifier)
- **title**: String (chapter title)
- **slug**: String (URL-friendly identifier)
- **content**: String (Markdown content of the chapter)
- **word_count**: Integer (number of words in the chapter)
- **learning_objectives**: Array<String> (list of objectives for the chapter)
- **key_concepts**: Array<String> (key terms and concepts covered)
- **prerequisites**: Array<String> (previous chapters or concepts needed)
- **related_chapters**: Array<String> (cross-references to related chapters)
- **exercises**: Array<Object> (practice questions/assignments)
- **metadata**: Object (creation date, last updated, author, etc.)

### Exercise Entity
- **id**: String (unique identifier)
- **type**: String (multiple_choice, short_answer, practical, etc.)
- **question**: String (the exercise question)
- **options**: Array<String> (for multiple choice questions)
- **answer**: String (correct answer)
- **explanation**: String (explanation of the answer)
- **difficulty**: String (beginner, intermediate, advanced)

## RAG System Data Models

### Document Chunk Entity
- **id**: String (unique identifier)
- **chapter_id**: String (reference to the chapter)
- **content**: String (text content of the chunk)
- **chunk_index**: Integer (position of the chunk in the chapter)
- **embedding**: Array<Float> (vector representation of the content)
- **metadata**: Object (source, section, etc.)

### Embedding Model Parameters
- **model_name**: String (name of the embedding model, e.g., "bge-small-en")
- **dimensions**: Integer (number of dimensions in the embedding vector)
- **max_length**: Integer (maximum token length for input)
- **normalization**: Boolean (whether embeddings are normalized)

### Query Result Entity
- **chunk_id**: String (ID of the matching chunk)
- **chapter_id**: String (ID of the chapter containing the chunk)
- **content**: String (text content of the matching chunk)
- **similarity_score**: Float (similarity score between query and chunk)
- **metadata**: Object (additional information about the match)

## User Interaction Models

### Query Entity
- **id**: String (unique identifier for the query)
- **user_input**: String (original query from the user)
- **processed_query**: String (cleaned and processed query)
- **timestamp**: DateTime (when the query was made)
- **user_preferences**: Object (complexity level, language preference if applicable)

### Response Entity
- **query_id**: String (reference to the original query)
- **response**: String (generated response to the query)
- **source_chunks**: Array<String> (IDs of chunks used to generate the response)
- **confidence**: Float (confidence level of the response)
- **timestamp**: DateTime (when the response was generated)

### User Preferences Entity
- **id**: String (unique identifier)
- **user_id**: String (identifier for the user, if applicable)
- **response_complexity**: String (beginner, intermediate, advanced)
- **language_preference**: String (default language, e.g., "en", "ur")
- **personalization_enabled**: Boolean (whether personalization is active)

## Validation Rules

### Content Validation
- Chapter word count must be between 800 and 1500 words
- Chapter title must not exceed 100 characters
- Content must be valid Markdown
- Learning objectives must be 3-5 items long
- All cross-references must point to existing chapters

### RAG System Validation
- Document chunks must not exceed 512 tokens
- Embedding vectors must match the expected dimensions for the model
- Similarity scores must be between 0 and 1
- Query must be at least 5 characters long

## State Transitions

### Content Review Process
1. **Draft** → Content is being written
2. **Reviewed** → Content has been reviewed for accuracy
3. **Approved** → Content is ready for publication
4. **Published** → Content is live on the site

### Query Processing Pipeline
1. **Received** → Initial query state
2. **Processed** → Query has been processed and validated
3. **Retrieved** → Relevant chunks have been retrieved
4. **Generated** → Response has been generated
5. **Delivered** → Response has been sent to the user

## Relationships

### Chapter Relationships
- Each chapter may have zero or more related chapters (cross-references)
- Each chapter contains multiple exercises
- Each chapter is divided into multiple document chunks for RAG

### Query Relationships
- Each query generates one response
- Each response is based on multiple document chunks
- Each document chunk belongs to exactly one chapter

## API Contract Models

### Query Request Model
```
{
  "query": "What is ROS 2?",
  "options": {
    "response_complexity": "beginner",
    "language": "en",
    "use_personalization": true
  }
}
```

### Query Response Model
```
{
  "response": "ROS 2 (Robot Operating System 2) is...",
  "source_chapters": ["ros2-fundamentals"],
  "confidence": 0.85,
  "chunks_used": 3
}
```

## Indexes and Performance Considerations

### Database Indexes
- Chapter slug for fast URL routing
- Chapter prerequisites and related chapters for navigation
- Document chunk embedding for fast similarity search
- Query timestamp for analytics

### RAG Performance
- Pre-computed embeddings for document chunks
- Efficient vector indexing in Qdrant
- Caching for frequently asked questions
- Asynchronous processing for complex queries