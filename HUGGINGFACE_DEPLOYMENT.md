# Hugging Face Space Deployment Guide

## Preparing for Hugging Face Deployment

Due to time and resource limitations on Hugging Face Spaces, you need to pre-compute embeddings before deploying.

### Step 1: Generate Embeddings Locally

First, run the precompute script on your local machine with your GEMINI_API_KEY:

```bash
# Make sure you have your GEMINI_API_KEY set in your environment
export GEMINI_API_KEY=your_api_key_here

# Run the precompute script to generate real embeddings
python backend/scripts/precompute_embeddings.py
```

This will create `data/chunks.pkl` and `data/embeddings.pkl` files with real embeddings from Gemini.

### Alternative Step 1: For Testing Without API Key

If you don't have a GEMINI_API_KEY available, you can use mock embeddings for testing:

```bash
# Run the mock precompute script to generate simulated embeddings
python backend/scripts/precompute_embeddings_mock.py
```

Note: This creates simulated embeddings and should only be used for testing purposes.

### Step 2: Include Precomputed Files in Your Repository

Make sure to commit the generated files to your repository:

```bash
git add data/chunks.pkl data/embeddings.pkl
git commit -m "Add precomputed embeddings"
git push
```

### Step 3: Update Environment Variables

In your Hugging Face Space settings, ensure you have the `GEMINI_API_KEY` environment variable set.

### Step 4: Deploy to Hugging Face

The Hugging Face Space will now use the precomputed embeddings, which significantly reduces startup time.

## Troubleshooting

If you still encounter timeout issues:
- Ensure your `data/` directory exists with the precomputed embeddings
- Check that the `USE_PRECOMPUTED_EMBEDDINGS` environment variable is set to `true` (default)
- Verify your `GEMINI_API_KEY` is properly configured

## Local Development

For local development, you can run the original app:

```bash
# To regenerate embeddings during development (requires GEMINI_API_KEY)
python backend/scripts/precompute_embeddings.py

# To run with mock embeddings for testing
python backend/scripts/precompute_embeddings_mock.py

# To run with precomputed embeddings (default)
python app.py

# To run without precomputed embeddings (for testing only)
USE_PRECOMPUTED_EMBEDDINGS=false python app.py
```