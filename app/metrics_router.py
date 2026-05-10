from fastapi import APIRouter
from fastapi.responses import Response
from app.metrics import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
