from app.trainer import generate_problem
from app.database import SessionLocal


def test_generate_problem_returns_valid_structure():
    db = SessionLocal()
    try:
        problem = generate_problem(db)
        assert problem.id > 0
        assert "?" in problem.question
        assert problem.answer > 0
    finally:
        db.close()


def test_generate_problem_creates_unique_ids():
    db = SessionLocal()
    try:
        problem1 = generate_problem(db)
        problem2 = generate_problem(db)
        assert problem1.id != problem2.id
    finally:
        db.close()


def test_generate_problem_answer_is_correct():
    db = SessionLocal()
    try:
        problem = generate_problem(db)
        question = problem.question

        if "+" in question:
            parts = question.replace(" = ?", "").split(" + ")
            expected = int(parts[0]) + int(parts[1])
        else:
            parts = question.replace(" = ?", "").split(" x ")
            expected = int(parts[0]) * int(parts[1])

        assert problem.answer == expected
    finally:
        db.close()
