<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0 (initial version)
Modified principles: N/A (new document)
Added sections: All sections (new document)
Removed sections: N/A
Templates requiring updates: N/A (initial constitution)
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity
All content must be clear, concise, and accessible to beginner and intermediate learners. Explanations should avoid unnecessary jargon and provide intuitive analogies to help readers grasp complex concepts.

### II. Accuracy
Technical content must be factually correct, based on official documentation, peer-reviewed sources, and verified implementations. All claims about AI, robotics, and software tools must be validated through reliable sources.

### III. Minimalism
Each chapter should be focused and efficient, with lengths between 800-1500 words. Content must eliminate fluff and redundancy, focusing only on essential knowledge needed for understanding Physical AI and Humanoid Robotics.

### IV. Accessibility
All tools, architectures, and code examples must work within free-tier limitations. The project should be accessible to users with limited computational resources and financial means.

### V. Grounding
The RAG chatbot must provide answers exclusively derived from the textbook content. All responses must be retrievable from the book's text without hallucination or external knowledge injection.

### VI. Educational Progression
Content must follow a logical learning path that progressively builds complexity. Earlier chapters should establish foundation knowledge required for understanding later material.

## Additional Constraints

- No paid tools or GPU-dependent examples allowed
- Minimal embedding size and compute usage requirements
- Fast local build times for Docusaurus site
- Chapters restricted to the six required topics only:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Optional bonuses: Urdu translation mode and personalized explanations (implement only if feasible within free-tier)

## Development Standards

### Writing & Content Standards:
- Tone: Beginner-friendly, encouraging, professional
- Language: Clear English with optional Urdu support
- Structure: Proper headings, bullet points, numbered steps, code blocks, tables
- Include: Practical code examples (Python/ROS), Mermaid diagrams where helpful, simple quizzes
- Avoid: GPU-heavy code, advanced math, unnecessary complexity

### Technical & Formatting Standards:
- Output: Clean Docusaurus-compatible Markdown (.md files)
- Code blocks: Properly fenced with language tags
- Images/Diagrams: Described via Mermaid or placeholder references
- Sidebar: Auto-generated and logical flow
- RAG preparation: Clear section headings and semantic chunks for lightweight embeddings

### Quality Measurements:
- Success measured by: Successful Docusaurus build, GitHub Pages deployment, accurate RAG responses
- Every output must be reviewed against this constitution
- Prioritize clarity and usability over completeness

## Governance

This constitution governs ALL future phases of the project (specify, plan, task, implement) to ensure consistency, quality, and alignment with project goals. All project decisions must comply with these principles. Amendments to this constitution require documentation of changes, approval from project maintainers, and appropriate migration plans for existing artifacts.

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13