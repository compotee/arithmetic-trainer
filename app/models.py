from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    password: str
    created_at: datetime = datetime.now()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Problem(BaseModel):
    id: int
    question: str
    answer: int


class CheckRequest(BaseModel):
    problem_id: int
    user_answer: int


class CheckResponse(BaseModel):
    correct: bool
    correct_answer: int


class StatsResponse(BaseModel):
    username: str
    total_attempts: int
    correct_attempts: int
    accuracy: float


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    accuracy: float
    