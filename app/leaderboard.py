from fastapi import APIRouter
from app.trainer import stats_db
from app.models import LeaderboardEntry

router = APIRouter()


@router.get("/", response_model=list[LeaderboardEntry])
def get_leaderboard():
    """Получить топ-10 игроков по точности"""
    leaderboard = []
    for username, stats in stats_db.items():
        if stats["total"] >= 5:  # Минимум 5 попыток для попадания в рейтинг
            accuracy = (stats["correct"] / stats["total"] * 100)
            leaderboard.append({"username": username, "accuracy": accuracy})

    leaderboard.sort(key=lambda x: x["accuracy"], reverse=True)
    top10 = leaderboard[:10]

    return [
        LeaderboardEntry(rank=i+1, username=entry["username"], accuracy=round(entry["accuracy"], 1))
        for i, entry in enumerate(top10)
    ]
