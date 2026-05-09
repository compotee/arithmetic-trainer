from fastapi import APIRouter, Depends
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attempt, User
from app.redis_client import redis_client
import json

router = APIRouter()


@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    cached = redis_client.get("leaderboard:top10")
    if cached:
        return json.loads(cached)

    results = (
        db.query(
            User.username,
            func.count(Attempt.id).label("total"),
            func.sum(case((Attempt.is_correct, 1), else_=0)).label("correct"),
        )
        .join(Attempt, User.id == Attempt.user_id)
        .group_by(User.id, User.username)
        .having(func.count(Attempt.id) >= 5)
        .all()
    )

    leaderboard = []
    for username, total, correct in results:
        correct_val = correct or 0
        accuracy = (correct_val / total * 100) if total > 0 else 0.0
        leaderboard.append({"username": username, "accuracy": round(accuracy, 1)})

    leaderboard.sort(key=lambda x: x["accuracy"], reverse=True)
    top10 = leaderboard[:10]

    result = [
        {"rank": i + 1, "username": entry["username"], "accuracy": entry["accuracy"]}
        for i, entry in enumerate(top10)
    ]

    redis_client.set("leaderboard:top10", json.dumps(result), ex=300)

    return result
