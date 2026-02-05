# AI Excuse Generator 🎭

> 不想上班？不想聚会？AI帮你找个完美的借口！

AI-powered excuse generator that helps you craft the perfect excuse for any situation.

## Features

- 🎯 **Smart Scenarios**: Pre-built scenarios for common situations
- 🤖 **AI Generation**: Natural, believable excuses powered by AI
- 🎨 **Style Options**: From sincere to absurdly funny
- 🌍 **7 Languages**: EN/ZH/JA/DE/FR/KO/ES support
- 📋 **One-Click Copy**: Easy sharing

## Tech Stack

- **Frontend**: React + Vite (TypeScript) + TailwindCSS
- **Backend**: Python FastAPI
- **AI**: LLM via llm-proxy.densematrix.ai
- **Deploy**: Docker

## Quick Start

```bash
# Clone
git clone https://github.com/densematrix-labs/ai-excuse-generator.git
cd ai-excuse-generator

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env with your keys
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## License

MIT
