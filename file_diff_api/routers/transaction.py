from sqlalchemy.orm.session import Session
from .schemas import TransactionBase, TransactionDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from db import db_transaction
from typing import List

router = APIRouter(
    prefix='/transaction',
    tags=['transaction']
)


@router.post('', response_model=TransactionDisplay)
def create_transaction(request: TransactionBase, db: Session = Depends(get_db)):
    return db_transaction.create_transaction(db, request)


@router.get('/all', response_model=List[TransactionDisplay])
def get_transaction(db: Session = Depends(get_db)):
    return db_transaction.get_all(db)


@router.get('/get/{comp_id}')
def get_transaction(comp_id: int, db: Session = Depends(get_db)):
    return db_transaction.get_transactions(comp_id, db)
