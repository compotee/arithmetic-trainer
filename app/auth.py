from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import datetime

router = APIRouter()
security = HTTPBearer()

# Временное хранилище (потом заменим на БД)
users_db = {}
SECRET_KEY = "test-secret-key"


@router.post("/register")
def register(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users_db[username] = password
    return {"message": "Регистрация успешна"}


@router.post("/login")
def login(username: str, password: str):
    if username not in users_db or users_db[username] != password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")
    