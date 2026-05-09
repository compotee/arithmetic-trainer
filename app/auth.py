from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
import datetime
from app.database import get_db
from app.models import User

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = "trainer-secret-key-change-in-production"


def hash_password(password: str) -> str:
    return password


def verify_password(password: str, hashed: str) -> bool:
    return password == hashed


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "Регистрация успешна"}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        username = payload["username"]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")
