# Local LLM Setup with Ollama

This guide shows how to set up Ollama for local LLM inference (free, no API key required).

## Step 1: Install Ollama

### macOS
```bash
# Option 1: Using Homebrew
brew install ollama

# Option 2: Download directly
# Visit https://ollama.ai and download the macOS installer
```

### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

### Windows
Download from https://ollama.ai

## Step 2: Download a Model

Start Ollama and download a model (first time takes 5-15 minutes depending on model size):

```bash
# Download Mistral (7B - recommended for speed)
ollama pull mistral

# OR download other models:
ollama pull neural-chat    # Good balance
ollama pull llama2          # Meta's Llama 2
ollama pull dolphin-mixtral # Excellent reasoning
```

## Step 3: Run Ollama

```bash
# Start the Ollama server (runs on http://localhost:11434)
ollama serve
```

The server will listen on `http://localhost:11434` by default.

## Step 4: Test It Works

In a new terminal, test the API:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Explain photosynthesis in 100 words",
  "stream": false
}'
```

## Step 5: Start Your Application

With Ollama running, start the backend:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Then start the frontend:

```bash
cd frontend
npm run dev
```

## Model Recommendations

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **mistral** | 7B | Fast | Good | Default choice |
| **neural-chat** | 7B | Fast | Good | Conversational |
| **llama2** | 7B/13B | Medium | Good | General purpose |
| **dolphin-mixtral** | 46B | Slow | Excellent | If you have 16GB+ RAM |

## Troubleshooting

### "connection refused" error
- Make sure Ollama is running: `ollama serve`
- Check it's accessible: `curl http://localhost:11434/api/tags`

### Slow responses
- Use a smaller model (mistral is fastest)
- Increase your system RAM or close other applications

### Model not found
- Pull the model: `ollama pull mistral`
- Check installed models: `ollama list`

## Switching Models

To use a different model, edit `backend/app/services/ai_service.py` and change the `MODEL` variable:

```python
MODEL = "neural-chat"  # Change this
```

Then restart the backend.
