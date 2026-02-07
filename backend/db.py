"""
Database connection and session management.

Handles connection to Neon PostgreSQL database with connection pooling.
"""
import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine with connection pooling
# pool_size: Number of connections to maintain in the pool
# max_overflow: Maximum number of connections that can be created beyond pool_size
# pool_pre_ping: Verify connections before using them (handles stale connections)
# pool_recycle: Recycle connections after 3600 seconds (1 hour) to prevent stale connections
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.

    Yields:
        Session: Database session
    """
    with Session(engine) as session:
        yield session
