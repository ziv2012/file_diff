from pydantic import BaseModel
from datetime import datetime
from typing import List


class RecordBase(BaseModel):
    comp_id: int
    diff_type: str
    property_type: str
    value_left: str
    value_right: str


class RecordDisplay(BaseModel):
    comp_id: int
    diff_type: str
    property_type: str
    value_left: str
    value_right: str

    class Config():
        orm_mode = True


class CompBase(BaseModel):
    left_name: str
    right_name: str
    comp_date: datetime


class CompDisplay(BaseModel):
    id: int
    left_name: str
    right_name: str
    comp_date: datetime

    class Config():
        orm_mode = True
