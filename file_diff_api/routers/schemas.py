from pydantic import BaseModel
from datetime import datetime
from typing import List


class TransactionBase(BaseModel):
    comp_id: int
    trans_id: str
    diff_type: str
    value_left: str
    value_right: str


class TransactionDisplay(BaseModel):
    id: int
    trans_id: str
    comp_id: int
    diff_type: str
    value_left: str
    value_right: str

    class Config():
        orm_mode = True


class CompBase(BaseModel):
    left_name: str
    right_name: str
    comp_date: datetime

    # def __init__(self, leftName, rightName, date):
    #     self.left_name = leftName
    #     self.right_name = rightName
    #     self.comp_date = date


class CompDisplay(BaseModel):
    id: int
    left_name: str
    right_name: str
    comp_date: datetime
    transactions: List[TransactionDisplay]

    class Config():
        orm_mode = True
