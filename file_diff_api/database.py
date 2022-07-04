from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:201220@localhost/file_diff_db"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# def get_db():
#     db = _database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
