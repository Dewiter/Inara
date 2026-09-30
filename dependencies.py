from typing import Any, Generator
from sqlalchemy.orm import sessionmaker
# from db.database import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Any, Any, Any]:
    """
    Get the database session.

    :return: Generator[Any, Any, Any]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
