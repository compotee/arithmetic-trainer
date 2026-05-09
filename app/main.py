from fastapi import FastAPI

# from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.auth import router as auth_router
from app.trainer import router as trainer_router
from app.leaderboard import router as leaderboard_router

app = FastAPI(title="Арифметический тренажёр")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(trainer_router, prefix="/trainer", tags=["trainer"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["leaderboard"])


@app.get("/")
def root():
    return FileResponse("app/templates/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


import os
