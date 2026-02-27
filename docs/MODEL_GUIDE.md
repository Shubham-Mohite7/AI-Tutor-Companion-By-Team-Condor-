# Model Performance Guide

If you're getting timeout errors, use a faster model:

## Current Setup
- **Model**: Mistral (7B)
- **Timeout**: 10 minutes (600 seconds)

## Faster Models (Recommended)

### Option 1: Use Phi (Fastest)
```bash
# Download Phi (2.7B - very fast)
ollama pull phi

# Then edit: backend/app/services/ai_service.py
# Change: MODEL = "phi"
```

### Option 2: Use Neural-Chat (Balanced)
```bash
# Download Neural-Chat (7B - good speed/quality)
ollama pull neural-chat

# Then edit: backend/app/services/ai_service.py
# Change: MODEL = "neural-chat"
```

### Option 3: Use Orca-Mini (Small but capable)
```bash
# Download Orca-Mini (3B)
ollama pull orca-mini

# Then edit: backend/app/services/ai_service.py
# Change: MODEL = "orca-mini"
```

## Model Comparison

| Model | Size | Speed | Quality | Recommended |
|-------|------|-------|---------|-------------|
| **phi** | 2.7B | Very Fast | Fair | Recommended If timeout |
| **orca-mini** | 3B | Fast | Good | Good balance |
| **neural-chat** | 7B | Medium | Good | If you have time |
| **mistral** | 7B | Medium | Excellent | Current |
| **llama2** | 7B/13B | Slow | Excellent | Large RAM needed |

## Steps to Switch Models

1. **Download new model**:
   ```bash
   ollama pull phi
   ```

2. **Update backend**:
   ```bash
   # Edit: /Users/shubham6699/Downloads/aitutor/backend/app/services/ai_service.py
   # Line: MODEL = "mistral"
   # Change to: MODEL = "phi"
   ```

3. **Restart backend**:
   ```bash
   cd /Users/shubham6699/Downloads/aitutor/backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

4. **Try the app again**

## If Still Timing Out

- Increase timeout in `ai_service.py`: change `timeout=600` to `timeout=1200`
- Close other applications to free up RAM
- Check Ollama is running: `curl http://localhost:11434/api/tags`
