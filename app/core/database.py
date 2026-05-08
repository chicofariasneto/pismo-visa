from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy ORM models."""


async def get_db() -> AsyncSession:
    """Yield an async database session for use as a FastAPI dependency.

    Opens a session from the connection pool, yields it to the caller,
    and ensures it is closed when the request finishes.

    :returns: An active async database session.
    :rtype: AsyncSession
    """
    async with AsyncSessionLocal() as session:
        yield session
