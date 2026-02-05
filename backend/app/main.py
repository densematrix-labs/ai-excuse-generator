from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import excuse_router, payment_router, token_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title="AI Excuse Generator",
    description="Generate perfect excuses for any situation!",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(excuse_router)
app.include_router(payment_router)
app.include_router(token_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-excuse-generator"}


@app.get("/")
async def root():
    return {
        "name": "AI Excuse Generator",
        "version": "1.0.0",
        "docs": "/docs"
    }
