from typing import List
from fastapi import HTTPException, status
from routers.schemas import TransactionBase
from sqlalchemy.orm.session import Session
from .models import DbTransaction


def create_transaction(db: Session, request: TransactionBase):
    new_trans = DbTransaction(
        comp_id=request.comp_id,
        trans_id=request.trans_id,
        diff_type=request.diff_type,
        value_left=request.value_left,
        value_right=request.value_right,
    )
    db.add(new_trans)
    db.commit()
    db.refresh(new_trans)
    return request


def get_all(db: Session):
    return db.query(DbTransaction).all()


def get_transactions(comp_id: int, db: Session):
    return db.query(DbTransaction).filter(DbTransaction.comp_id == comp_id).all()
