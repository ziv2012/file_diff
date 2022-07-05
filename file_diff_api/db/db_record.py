from fastapi import HTTPException, status
from routers.schemas import RecordBase
from sqlalchemy.orm.session import Session
from .models import DbRecord


def create_rec(db: Session, request: RecordBase):
    new_rec = DbRecord(
        comp_id=request.comp_id,
        diff_type=request.diff_type,
        property_type=request.property_type,
        value_left=request.value_left,
        value_right=request.value_right,
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec


def get_all(db: Session):
    return db.query(DbRecord).all()
# def get_user_by_username(db: Session,username: str):
#     user = db.query(DbRecord).filter(DbRecord.username == username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail = f'User with username {username} not found')
#     return user
