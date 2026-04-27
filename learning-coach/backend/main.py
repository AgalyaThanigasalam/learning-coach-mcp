from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import questions, answers, chat, progress, learning_path, analytics, upload
from app.api import revision, leaderboard

app = FastAPI(
    title="Personalized Learning Coach API",
    description="AI-powered adaptive learning platform with 7 MCP tools",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router,     prefix="/api", tags=["Questions"])
app.include_router(answers.router,       prefix="/api", tags=["Answers"])
app.include_router(chat.router,          prefix="/api", tags=["Chat"])
app.include_router(progress.router,      prefix="/api", tags=["Progress"])
app.include_router(learning_path.router, prefix="/api", tags=["Learning Path"])
app.include_router(analytics.router,     prefix="/api", tags=["Analytics"])
app.include_router(upload.router,        prefix="/api", tags=["Upload"])
app.include_router(revision.router,      prefix="/api", tags=["Revision"])
app.include_router(leaderboard.router,   prefix="/api", tags=["Leaderboard"])

@app.get("/")
async def root():
    return {"message": "Personalized Learning Coach API v2.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
