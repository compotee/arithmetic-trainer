from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from app.metrics import http_requests_total, http_request_duration_seconds
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
from app.auth import router as auth_router
from app.trainer import router as trainer_router
from app.leaderboard import router as leaderboard_router
from app.database import engine, Base

app = FastAPI(title="Арифметический тренажёр")

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    http_requests_total.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()
    http_request_duration_seconds.labels(endpoint=request.url.path).observe(duration)
    return response


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(trainer_router, prefix="/trainer", tags=["trainer"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["leaderboard"])


@app.get("/")
def root():
    return FileResponse("app/templates/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
