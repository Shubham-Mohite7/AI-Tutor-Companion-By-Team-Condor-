# 🆘 Troubleshooting Guide - AITutor

## Issue: "Load failed" Error

### Problem
When clicking "Start Learning", the page shows "Load failed" instead of generating the explanation and quiz.

### Solution

#### Step 1: Verify Backend is Running
```bash
# Test the backend health endpoint
curl http://localhost:8000/api/v1/tutor/health

# Expected output:
# {"status":"ok"}
```

If this fails, the backend is not running. Go to Step 2.

#### Step 2: Start the Backend

**Option A: Fresh Start (Recommended)**
```bash
# Navigate to backend directory
cd /Users/shubham6699/Downloads/aitutor/backend

# Start the backend
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --port 8000 &

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

**Option B: With Reload Mode (for development)**
```bash
cd /Users/shubham6699/Downloads/aitutor/backend
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

#### Step 3: Verify Frontend is Running
```bash
# Check if Next.js is running
ps aux | grep "next dev" | grep -v grep

# If not running, start it:
cd /Users/shubham6699/Downloads/aitutor/frontend
npm run dev

# You should see:
# Ready in X.Xs
# - Local: http://localhost:3000 (or 3001 if 3000 is taken)
```

#### Step 4: Open the App
- **If frontend on 3000**: Open http://localhost:3000
- **If frontend on 3001**: Open http://localhost:3001

#### Step 5: Clear Browser Cache (Optional)
If you still see errors:
1. Open DevTools (F12 or Cmd+Shift+I)
2. Go to Application → Cache Storage → Clear all
3. Go to Application → Cookies → Delete all
4. Reload page (Cmd+R)

---

## Common Errors & Fixes

### Error: "Cannot connect to backend"
**Cause**: Backend service is not running on port 8000
**Fix**: 
```bash
# Kill any existing processes
pkill -f uvicorn

# Start fresh
cd /Users/shubham6699/Downloads/aitutor/backend
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --port 8000 &
```

### Error: "OPENROUTER_API_KEY not set"
**Cause**: API key missing in `.env` file
**Fix**:
```bash
# Check if .env exists
cat /Users/shubham6699/Downloads/aitutor/backend/.env | grep OPENROUTER

# If empty or missing, add the key:
echo "OPENROUTER_API_KEY=your_actual_api_key_here" >> src/backend/.env

# Restart backend
pkill -f uvicorn
# Then start backend again
```

### Error: "ModuleNotFoundError: No module named 'app'"
**Cause**: Running uvicorn from wrong directory
**Fix**:
```bash
# Make sure you're in the backend directory
cd /Users/shubham6699/Downloads/aitutor/backend

# Then run uvicorn
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --port 8000
```

### Error: "Port 8000 already in use"
**Cause**: Something else is using port 8000
**Fix**:
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace XXXX with PID)
kill -9 XXXX

# Or use different port
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --port 8001

# Then update frontend API URL in .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > /Users/shubham6699/Downloads/aitutor/frontend/.env.local
```

### Error: "Frontend not loading / Shows 'I could not compile this app'"
**Cause**: Frontend build error or not running
**Fix**:
```bash
# Navigate to frontend
cd /Users/shubham6699/Downloads/aitutor/frontend

# Clean install
rm -rf node_modules .next
npm install

# Start dev server
npm run dev
```

---

## Quick Startup Script

Save this as `/Users/shubham6699/Downloads/aitutor/start.sh`:

```bash
#!/bin/bash

echo "Starting AiTutor..."

# Terminal 1: Backend
echo "Starting backend on port 8000..."
cd /Users/shubham6699/Downloads/aitutor/backend
/Users/shubham6699/Downloads/aitutor/backend/venv/bin/python -m uvicorn app.main:app --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 2

# Terminal 2: Frontend
echo "Starting frontend..."
cd /Users/shubham6699/Downloads/aitutor/frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "AiTutor is running!"
echo "Open: http://localhost:3000 (or 3001)"
echo ""
echo "To stop:"
echo "  kill $BACKEND_PID   # Stop backend"
echo "  kill $FRONTEND_PID  # Stop frontend"
echo ""
```

**Usage:**
```bash
chmod +x /Users/shubham6699/Downloads/aitutor/start.sh
/Users/shubham6699/Downloads/aitutor/start.sh
```

---

## Verify Everything is Working

### 1. Backend Health Check
```bash
curl http://localhost:8000/api/v1/tutor/health
# Should return: {"status":"ok"}
```

### 2. Frontend is Responsive
```bash
curl http://localhost:3000/
# Should return HTML
```

### 3. API Integration
Open browser DevTools (F12) and:
1. Go to Network tab
2. Enter a topic and click "Start Learning"
3. You should see requests to:
   - `POST /api/v1/tutor/learn`
   - Response should have explanation and quiz

### 4. Check Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Look for any red errors
4. Common issues:
   - `Failed to fetch from http://localhost:8000` → Backend not running
   - `CORS error` → Check CORS settings in backend
   - `Cannot read property 'questions'` → API response format wrong

---

## Process Management

### See All Running Processes
```bash
# Backend
ps aux | grep uvicorn

# Frontend  
ps aux | grep "next dev"
```

### Kill All Related Processes
```bash
# Kill all Python/Uvicorn processes
pkill -f uvicorn

# Kill all Node/Next processes
pkill -f "next dev"

# Kill all Node processes (careful!)
killall node
```

### Monitor Logs
```bash
# Backend logs (if running in background)
tail -f /tmp/backend.log

# Frontend logs
# Check browser DevTools → Console
```

---

## Environment Variables

### Backend (.env)
```env
DEBUG=false
OPENROUTER_API_KEY=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
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Testing the Feature

### Standard Quiz
1. Enter topic
2. Click "Standard Quiz" button
3. Answer MCQ questions
4. Submit for score

### Adaptive Quiz
1. Enter topic
2. Click "Adaptive Practice"
3. Answer questions (difficulty adapts)
4. Keep going until satisfied

### True/False Swipe Cards
1. Enter topic
2. Click "↔️ Swipe Cards"
3. Swipe right for TRUE, left for FALSE
4. See score

---

## Performance Tips

### If App is Slow
1. **Close other tabs** - Free up browser memory
2. **Clear cache** - DevTools → Application → Clear Storage
3. **Restart backend** - Fresh connection
4. **Check network** - DevTools → Network tab → Look for slow requests
5. **Update OpenRouter key** - Ensure it has credits

### If Responses are Slow (5+ seconds)
1. **OpenRouter is slow** - Normal for cloud API
2. **Network issue** - Check internet connection
3. **Backend overloaded** - Restart backend
4. **Try different model** - Check backend config

---

## Getting Help

If issues persist:

1. **Check logs**
   - Backend: Look at terminal output
   - Frontend: DevTools → Console tab

2. **Test each component**
   ```bash
   # Test backend
   curl http://localhost:8000/api/v1/tutor/health
   
   # Test API endpoint
   curl -X POST http://localhost:8000/api/v1/tutor/learn \
     -H "Content-Type: application/json" \
     -d '{"topic": "Python", "language": "en"}'
   ```

3. **Check configuration**
   - API key in `.env`?
   - Port 8000 free?
   - Port 3000/3001 free?
   - Node/Python versions OK?

4. **Last resort: Fresh reinstall**
   ```bash
   # Backend
   cd /Users/shubham6699/Downloads/aitutor/backend
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Frontend
   cd /Users/shubham6699/Downloads/aitutor/frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## Quick Reference

| Issue | Command |
|-------|---------|
| Backend not running | `cd backend && venv/bin/python -m uvicorn app.main:app --port 8000` |
| Frontend not running | `cd frontend && npm run dev` |
| Port 8000 in use | `lsof -i :8000` then `kill -9 PID` |
| Clear Node cache | `cd frontend && rm -rf .next node_modules && npm install` |
| Test backend | `curl http://localhost:8000/api/v1/tutor/health` |
| Check logs | `cd backend && tail -f app/main.py` |
| Browser cache | DevTools → Application → Storage → Clear All |

---

**You're all set! The app should now work perfectly.**

Open http://localhost:3001 and start learning!
