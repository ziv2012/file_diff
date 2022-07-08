from sqlalchemy.orm.session import Session
from .schemas import TransactionBase, TransactionDisplay, CreateTransaction
from fastapi import APIRouter, Depends
from db.database import get_db
from db import db_transaction
from typing import List

router = APIRouter(
    prefix='/transaction',
    tags=['transaction']
)


@router.post('', response_model=TransactionBase)
def create_transaction(trans: CreateTransaction, db: Session = Depends(get_db)):
    return db_transaction.create_transaction(db, trans)


@router.get('/all', response_model=List[TransactionDisplay])
def get_transaction(db: Session = Depends(get_db)):
    return db_transaction.get_all(db)


@router.get('/get/{comp_id}')
def get_transaction(comp_id: int, db: Session = Depends(get_db)):
    return db_transaction.get_transactions(comp_id, db)


@router.post('/BULK')
def create_transaction(request: List[TransactionBase], db: Session = Depends(get_db)):
    return db_transaction.bulk_insert(db, request)
