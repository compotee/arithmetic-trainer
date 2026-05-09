from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_new_user():
    """Тест регистрации нового пользователя"""
    response = client.post("/auth/register?username=testuser&password=testpass")
    assert response.status_code == 200
    assert response.json() == {"message": "Регистрация успешна"}


def test_register_duplicate_user():
    """Тест регистрации дубликата"""
    client.post("/auth/register?username=user2&password=pass")
    response = client.post("/auth/register?username=user2&password=pass")
    assert response.status_code == 400


def test_login_success():
    """Тест успешного входа"""
    client.post("/auth/register?username=loginuser&password=testpass")
    response = client.post("/auth/login?username=loginuser&password=testpass")
    assert response.status_code == 200
    assert "access_token" in response.json()
    