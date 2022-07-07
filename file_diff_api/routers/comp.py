from sqlalchemy.orm.session import Session
from .schemas import CompBase, CompDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from db import db_comp
from typing import List

router = APIRouter(
    prefix='/comp',
    tags=['comp']
)


@router.post('', response_model=CompDisplay)
def create_comp(request: CompBase, db: Session = Depends(get_db)):
    return db_comp.create_comp(db, request)


@router.get('/all', response_model=List[CompDisplay])
def get_comp(db: Session = Depends(get_db)):
    return db_comp.get_all(db)
