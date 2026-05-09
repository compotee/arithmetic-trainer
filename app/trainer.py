from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models import Problem, CheckRequest, CheckResponse, StatsResponse
import random

router = APIRouter()

# Хранилище задач и статистики (потом заменим на БД)
problems_db = {}
stats_db = {}


def generate_problem():
    """Генерирует случайный пример на сложение или умножение"""
    if random.random() > 0.5:
        num1, num2 = random.randint(100, 999), random.randint(100, 999)
        question = f"{num1} + {num2} = ?"
        answer = num1 + num2
    else:
        num1, num2 = random.randint(10, 99), random.randint(10, 99)
        question = f"{num1} x {num2} = ?"
        answer = num1 * num2

    problem_id = len(problems_db) + 1
    problems_db[problem_id] = answer
    return Problem(id=problem_id, question=question, answer=answer)


@router.get("/problem", response_model=Problem)
def get_problem(username: str = Depends(get_current_user)):
    """Получить новый пример"""
    return generate_problem()


@router.post("/check", response_model=CheckResponse)
def check_answer(request: CheckRequest, username: str = Depends(get_current_user)):
    """Проверить ответ"""
    if request.problem_id not in problems_db:
        return CheckResponse(correct=False, correct_answer=0)

    correct_answer = problems_db[request.problem_id]
    is_correct = request.user_answer == correct_answer

    # Сохраняем статистику
    if username not in stats_db:
        stats_db[username] = {"total": 0, "correct": 0}
    stats_db[username]["total"] += 1
    if is_correct:
        stats_db[username]["correct"] += 1

    return CheckResponse(correct=is_correct, correct_answer=correct_answer)


@router.get("/stats", response_model=StatsResponse)
def get_stats(username: str = Depends(get_current_user)):
    """Получить статистику пользователя"""
    stats = stats_db.get(username, {"total": 0, "correct": 0})
    accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0.0

    return StatsResponse(
        username=username,
        total_attempts=stats["total"],
        correct_attempts=stats["correct"],
        accuracy=round(accuracy, 1),
    )
