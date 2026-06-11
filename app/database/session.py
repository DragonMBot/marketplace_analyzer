from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings
from app.core.logger import logger


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)


# ============================================================
# SESSION FACTORY
# ============================================================

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


# ============================================================
# DEPENDENCY FOR FASTAPI (optional but recommended)
# ============================================================

async def get_db() -> AsyncSession:
    """
    FastAPI dependency for DB session.
    """

    async with async_session_factory() as session:
        try:
            yield session
        except Exception as exc:
            logger.exception(f"DB session error: {exc}")
            await session.rollback()
            raise
        finally:
            await session.close()