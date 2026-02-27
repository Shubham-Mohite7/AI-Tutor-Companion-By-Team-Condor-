# AITutor — Production-Ready Web App

Tutor for Indian students. Enter any topic, get a clear explanation, then take a 10-question mock test grounded in that explanation.

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| Backend   | FastAPI, Python 3.12, Pydantic v2       |
| API        | OpenRouter → GPT-OSS 120B (deep reasoning) |
| Deploy    | Docker + docker-compose                 |

## Project Structure

```
aitutor/
├── backend/
│   ├── app/
│   │   ├── core/config.py          # Settings (pydantic-settings)
│   │   ├── models/schemas.py       # Request/response Pydantic models
│   │   ├── services/api_service.py  # All API logic isolated here
│   │   ├── api/routes/tutor.py     # FastAPI route handlers
│   │   └── main.py                 # App factory + middleware
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
└── frontend/
    ├── app/
    │   ├── components/
    │   │   ├── layout/             # Navbar, Hero
    │   │   ├── ui/                 # Card, Button (reusable)
    │   │   └── tutor/              # TutorApp, TopicInput, QuizView, etc.
    │   ├── hooks/useLearn.ts       # All client state + API calls
    │   ├── lib/api.ts              # Typed fetch wrapper
    │   ├── types/index.ts          # Shared TypeScript types
    │   ├── layout.tsx
    │   └── page.tsx
    ├── public/manifest.json
    ├── tailwind.config.ts
    ├── next.config.mjs
    └── Dockerfile
```

## Quick Start (Local Dev)

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edit .env — set your OPENROUTER_API_KEY

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
# API docs → http://localhost:8000/docs
```

### 2. Frontend

```bash
cd frontend
cp .env.local.example .env.local

npm install
npm run dev
# App → http://localhost:3000
```

## Docker (Production)

```bash
# Set your API key in backend/.env first
docker-compose up --build
```

Frontend → http://localhost:3000  
Backend API docs → http://localhost:8000/docs

## API Endpoints

| Method | Path                    | Description                          |
|--------|-------------------------|--------------------------------------|
| POST   | /api/v1/tutor/learn     | Generate explanation + quiz (30-60s) |
| POST   | /api/v1/tutor/score     | Score quiz answers (instant)         |
| GET    | /api/v1/tutor/health    | Health check                         |
| GET    | /docs                   | Swagger UI                           |

### POST /api/v1/tutor/learn
```json
{ "topic": "Photosynthesis", "language": "en" }
```

### POST /api/v1/tutor/score
```json
{
  "quiz": [ /* array of QuizQuestion objects */ ],
  "answers": ["A) ...", "True", null, ...]
}
```

## Environment Variables

### Backend (`backend/.env`)
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEBUG=false
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
# AiTutor
