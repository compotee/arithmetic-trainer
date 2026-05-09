from app.trainer import generate_problem


def test_generate_problem_returns_valid_structure():
    """Проверяем, что generate_problem возвращает корректную структуру"""
    problem = generate_problem()
    assert problem.id > 0
    assert "?" in problem.question
    assert problem.answer > 0


def test_generate_problem_creates_unique_ids():
    """Проверяем, что ID уникальны"""
    problem1 = generate_problem()
    problem2 = generate_problem()
    assert problem1.id != problem2.id


def test_generate_problem_answer_is_correct():
    """Проверяем, что ответ соответствует примеру"""
    problem = generate_problem()
    question = problem.question

    if "+" in question:
        parts = question.replace(" = ?", "").split(" + ")
        expected = int(parts[0]) + int(parts[1])
    else:
        parts = question.replace(" = ?", "").split(" x ")
        expected = int(parts[0]) * int(parts[1])

    assert problem.answer == expected
    