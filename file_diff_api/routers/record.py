from sqlalchemy.orm.session import Session
from .schemas import RecordBase, RecordDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from db import db_record
from typing import List

router = APIRouter(
    prefix='/record',
    tags=['record']
)


@router.post('', response_model=RecordDisplay)
def create_record(request: RecordBase, db: Session = Depends(get_db)):
    return db_record.create_rec(db, request)


@router.get('/all', response_model=List[RecordDisplay])
def posts(db: Session = Depends(get_db)):
    return db_record.get_all(db)
