from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings


engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True, future=True)

# объект сессии асинхронного взаимодействия с базой данных

assync_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        session: AsyncSession = assync_session()
        yield session
    finally:
        await session.close()
