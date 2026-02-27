# AITutor - Project Structure

## 📁 Folder Organization

```
aitutor/
├── 📄 README.md                 # Main project documentation
├── 📄 .gitignore               # Git ignore rules
├── 📁 .github/                 # GitHub workflows
│   └── workflows/
│       ├── ci.yml             # CI/CD pipeline
│       └── docker.yml         # Docker build and push
├── 📁 src/                    # Source code
│   ├── 📁 backend/            # FastAPI backend application
│   │   ├── app/
│   │   │   ├── core/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   └── api/
│   │   ├── venv/               # Python virtual environment
│   │   ├── requirements.txt    # Python dependencies
│   │   ├── Dockerfile          # Backend Docker configuration
│   │   └── .env.example        # Environment variables template
│   └── 📁 frontend/           # Next.js frontend application
│       ├── app/
│       │   ├── components/
│       │   ├── hooks/
│       │   ├── lib/
│       │   └── types/
│       ├── public/
│       ├── Dockerfile          # Frontend Docker configuration
│       ├── package.json        # Node.js dependencies
│       └── .env.example        # Environment variables template
├── 📁 scripts/                # Utility scripts
│   ├── setup.sh               # Initial setup script
│   ├── start.sh               # Development startup script
│   ├── package.json           # Node.js package management
│   └── package-lock.json      # Locked dependencies
├── 📁 deployment/             # Deployment configurations
│   └── docker-compose.yml     # Development Docker setup
├── 📁 config/                 # Configuration files
│   └── docker-compose.prod.yml # Production Docker setup
├── 📁 docs/                   # Documentation
│   ├── README.md              # Main README (copied to root)
│   ├── SYSTEM_STATUS.md       # System status guide
│   ├── TROUBLESHOOTING.md     # Troubleshooting guide
│   ├── SWIPE_CARDS_GUIDE.md   # UI component guide
│   └── [other docs...]        # Additional documentation
├── 📁 hackathon/              # Hackathon-specific files
│   └── README.md              # Hackathon project description
├── 📁 assets/                 # Static assets
│   └── README.md              # Assets documentation
└── 📁 node_modules/           # Node.js dependencies (auto-generated)
```

## Quick Start

### 1. Setup
```bash
# Clone the repository
git clone <repository-url>
cd aitutor

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Configure
```bash
# Add your OpenRouter API key
echo "OPENROUTER_API_KEY=your_key_here" >> src/backend/.env
```

### 3. Start Development
```bash
# Start both frontend and backend
./scripts/start.sh
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Architecture

### Backend (FastAPI)
- **Port**: 8000
- **Framework**: FastAPI with Python 3.12
- **Main Components**:
  - `app/core/config.py` - Configuration management
  - `app/models/schemas.py` - Data models
  - `app/services/api_service.py` - External API integration
  - `app/api/routes/tutor.py` - API endpoints

### Frontend (Next.js)
- **Port**: 3000
- **Framework**: Next.js 14 with TypeScript
- **Main Components**:
  - `app/components/` - React components
  - `app/hooks/` - Custom React hooks
  - `app/lib/` - Utility functions
  - `app/types/` - TypeScript definitions

## Development Workflow

### Local Development
1. Backend: `uvicorn app.main:app --reload --port 8000`
2. Frontend: `npm run dev`
3. Both: `./scripts/start.sh`

### Production Deployment
```bash
# Using Docker
docker-compose -f config/docker-compose.prod.yml up -d
```

### CI/CD
- **GitHub Actions**: Automated testing and deployment
- **Docker**: Containerized deployment
- **Health Checks**: Automated monitoring

## Key Files

| File | Purpose |
|------|---------|
| `scripts/setup.sh` | Initial project setup |
| `scripts/start.sh` | Development server startup |
| `src/backend/.env.example` | Backend environment template |
| `src/frontend/.env.example` | Frontend environment template |
| `deployment/docker-compose.yml` | Development Docker setup |
| `config/docker-compose.prod.yml` | Production Docker setup |

## 🎯 Next Steps

1. **Environment Setup**: Run the setup script
2. **API Configuration**: Add your OpenRouter API key
3. **Development**: Use start script for local development
4. **Deployment**: Use Docker for production deployment

---

*This structure follows GitHub and hackathon best practices for web applications.*
