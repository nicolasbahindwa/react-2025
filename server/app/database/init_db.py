from app.database.session import engine
from app.database.base import Base


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Function to drop tables
async def drop_tables():
    """Drop all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Optional: Initialize database
async def init_db():
    """Initialize the database with tables."""
    try:
        await create_tables()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise