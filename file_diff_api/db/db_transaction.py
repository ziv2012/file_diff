from typing import List
from fastapi import HTTPException, status
from routers.schemas import TransactionBase, CreateTransaction, TransactionDisplay
from sqlalchemy.orm.session import Session
from .models import DbTransaction


def get_transactions(comp_id: int, db: Session):
    return db.query(DbTransaction).filter(DbTransaction.comp_id == comp_id).all()


def bulk_insert(db: Session, request: List[TransactionBase]):
    new_list = []
    for i in request:
        new_trans = DbTransaction(
            comp_id=i.comp_id,
            trans_id=i.trans_id,
            diff_type=i.diff_type,
            value_left=i.value_left,
            value_right=i.value_right,)
        new_list.append(new_trans)
    db.bulk_save_objects(new_list)
    db.commit()
    return new_list
