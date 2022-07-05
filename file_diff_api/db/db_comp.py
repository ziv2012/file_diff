from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import CompBase
from sqlalchemy.orm.session import Session
from .models import DbComparison


def create_comp(db: Session, request: CompBase):
    new_comp = DbComparison(
        left_name=request.left_name,
        right_name=request.right_name,
        comp_date=datetime.now(),
    )
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return new_comp


def get_all(db: Session):
    return db.query(DbComparison).all()
# def get_user_by_username(db: Session,username: str):
#     user = db.query(DbRecord).filter(DbRecord.username == username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail = f'User with username {username} not found')
#     return user
