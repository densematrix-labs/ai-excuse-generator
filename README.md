# AI Excuse Generator 🎭

Generate creative, believable excuses for any situation using AI. Like having a clever friend who always knows what to say!

## Features

- 🎯 **8 Excuse Categories**: Late, Sick Leave, Declining Invitations, Forgetting Things, Missing Deadlines, Missing Meetings, Homework, and Other
- 🎭 **3 Drama Levels**: Normal (believable), Urgent (slightly dramatic), Extreme (wild and theatrical!)
- 🌍 **7 Languages**: English, Chinese, Japanese, German, French, Korean, Spanish
- 💳 **Pay-per-use**: Free trial + affordable token packs

## Tech Stack

- **Frontend**: React + Vite + TypeScript
- **Backend**: Python FastAPI
- **AI**: Gemini 3 Flash Preview (via llm-proxy)
- **Styling**: Custom CSS with Retro Typewriter aesthetic

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend
cd backend
pytest --cov=app --cov-report=term-missing

# Frontend
cd frontend
npm run test:coverage
```

## Docker

```bash
docker-compose up --build
```

Access at http://localhost:3010

## Live Demo

https://excuse.demo.densematrix.ai

## License

MIT
