from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./notes.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create declarative base
Base = declarative_base()

# Dependency to get database session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Cleanup database
async def cleanup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
