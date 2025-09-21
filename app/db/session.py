from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
