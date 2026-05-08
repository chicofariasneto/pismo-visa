from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """Verify that the API and its database connection are operational.

    Executes a lightweight ``SELECT 1`` query to confirm the database is
    reachable. Returns HTTP 200 on success or HTTP 503 if the database
    cannot be reached.

    :param db: Injected async database session.
    :type db: AsyncSession
    :returns: A dict with ``status`` and ``version`` keys.
    :rtype: dict
    :raises HTTPException: 503 if the database connection fails.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "version": settings.app_version}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "version": settings.app_version},
        )
