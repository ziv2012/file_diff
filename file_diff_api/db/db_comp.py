from datetime import datetime
from fastapi import HTTPException, status
from routers.schemas import CompBase, CreateComp
from sqlalchemy.orm.session import Session
from .models import DbComparison


def create_comp(db: Session, request: CreateComp):
    new_comp = DbComparison(
        left_name=request.left_name,
        right_name=request.right_name,
        comp_date=datetime.now(),
    )
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return new_comp.id


def get_all(db: Session):
    return db.query(DbComparison).all()
