from fastapi import APIRouter, Response, status

from app.core.database import ping_database

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness():
    """Process is responsive. Never checks dependencies."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness(response: Response):
    """Can this pod serve traffic? Checks dependencies."""
    db_ok = await ping_database()

    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready", "mongodb": "unreachable"}

    return {"status": "ready", "mongodb": "connected"}
