from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random
from app.database import get_db
from app.models import Problem, Attempt, User
from app.auth import get_current_user

router = APIRouter()


def generate_problem(db: Session) -> Problem:
    if random.random() > 0.5:
        num1, num2 = random.randint(100, 999), random.randint(100, 999)
        question = f"{num1} + {num2} = ?"
        answer = num1 + num2
    else:
        num1, num2 = random.randint(10, 99), random.randint(10, 99)
        question = f"{num1} x {num2} = ?"
        answer = num1 * num2

    problem = Problem(question=question, answer=answer)
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


@router.get("/problem")
def get_problem(
    username: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    return generate_problem(db)


@router.post("/check")
def check_answer(
    problem_id: int,
    user_answer: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        return {"correct": False, "correct_answer": 0}

    is_correct = user_answer == problem.answer

    attempt = Attempt(
        user_id=user.id,
        problem_id=problem_id,
        user_answer=user_answer,
        is_correct=is_correct,
    )
    db.add(attempt)
    db.commit()

    return {"correct": is_correct, "correct_answer": problem.answer}


@router.get("/stats")
def get_stats(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {
            "username": username,
            "total_attempts": 0,
            "correct_attempts": 0,
            "accuracy": 0.0,
        }

    total = db.query(Attempt).filter(Attempt.user_id == user.id).count()
    correct = (
        db.query(Attempt).filter(Attempt.user_id == user.id, Attempt.is_correct).count()
    )
    accuracy = (correct / total * 100) if total > 0 else 0.0

    return {
        "username": username,
        "total_attempts": total,
        "correct_attempts": correct,
        "accuracy": round(accuracy, 1),
    }
