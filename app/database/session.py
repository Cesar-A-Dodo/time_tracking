from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

sqlite_path = os.getenv("SQLITE_PATH", "./app.db")
DATABASE_URL = f"sqlite:///{sqlite_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
