from pydantic import BaseModel
from datetime import datetime
from typing import List


class TransactionBase(BaseModel):
    comp_id: int
    trans_id: str
    diff_type: str
    value_left: str
    value_right: str


class TransactionDisplay(TransactionBase):
    id: int

    class Config():
        orm_mode = True


class CreateTransaction(TransactionBase):
    pass


class CompBase(BaseModel):
    left_name: str
    right_name: str
    comp_date: datetime


class CompDisplay(CompBase):
    id: int
    transactions: List[TransactionDisplay]

    class Config():
        orm_mode = True


class CreateComp(CompBase):
    pass
