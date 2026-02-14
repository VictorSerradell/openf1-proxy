# archivo: routers/health.py
from fastapi import APIRouter
import time

router = APIRouter(tags=["Health"])

START_TIME = time.time()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    return {
        "status": "ready",
        "uptime_seconds": int(time.time() - START_TIME),
    }
