from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .database import init_db
from .routers import auth, quiz, comments, stats
from .models import Base, User, Quiz, QuizAnswer, QuizAttempt, Comment, QuizStats

load_dotenv()

app = FastAPI(title="YellowBear Quiz API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(comments.router)
app.include_router(stats.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    await init_db()
