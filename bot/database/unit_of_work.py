from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @asynccontextmanager
    async def atomic(self):
        session: AsyncSession = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()