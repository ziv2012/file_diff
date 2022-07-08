from collections import defaultdict
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import false, true
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import List
import csv
from io import StringIO
from operator import itemgetter
from datetime import datetime
# from .schemas import CompBase, CompDisplay, TransactionBase, TransactionDisplay
from db import db_comp, db_transaction
from dataclasses import dataclass
from routers.schemas import CompBase


router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


class DiffType(str):
    ONLY_LEFT = "ONLY_LEFT"
    ONLY_RIGHT = "ONLY_RIGHT"


@dataclass
class Transaction:
    id: str
    amount: int
    currency: str
    date: datetime


@dataclass
class DiffObj:
    id: str
    comp_id: int
    diff_type: DiffType
    value_left: str
    value_right: str


def readCSV(contents: bytes):
    dict = defaultdict()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict[key] = rows
    buffer.close()
    return dict


def whatever(dict1: defaultdict, dict2: defaultdict):
    ds = [dict1, dict2]
    d = defaultdict()
    for k in set(list(dict1.keys()) + list(dict2.keys())):
        d[k] = tuple(d.get(k) for d in ds)

    for t in d.values():
        match t:
            case (None, t2):
                return DiffObj(id=t2.id, diff_type=DiffType.ONLY_RIGHT, value_left=None, value_right=None)
            case (t1, None):
                return DiffObj(id=t2.id, diff_type=DiffType.ONLY_LEFT, value_left=None, value_right=None)
            case (t1, t2):
                return DiffType.ONLY_LEFT


def createOutput(diff_keys: List[tuple]):
    resultList = []
    for rows in diff_keys:
        left, right = rows
        if left['id'] != right['id']:
            resultList.append(
                {"trans_id": left['id'], "diff_type": DiffType.ONLY_LEFT, "value_left": "", "value_right": ""})
            resultList.append(
                {"trans_id": right['id'], "diff_type": DiffType.ONLY_RIGHT, "value_left": "", "value_right": ""})
        else:
            mismatchkeys = {key for key in left.keys(
            ) & right if left[key] != right[key]}
            for x in mismatchkeys:
                resultList.append({"trans_id": left['id'], "diff_type": x, "value_left": left.get(
                    x), "value_right": right.get(x)})
    return resultList


@router.post('')
async def upload(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    # READ AND CONVERT BOTH FILES TO DICT
    dict1 = defaultdict()
    dict2 = defaultdict()
    contents = await files[0].read()
    dict1 = readCSV(contents)
    contents = await files[1].read()
    dict2 = readCSV(contents)

    list1 = list(dict1.values())
    list2 = list(dict2.values())

    # SORT LISTS
    list1, list2 = [sorted(l, key=itemgetter('id'))
                    for l in (list1, list2)]

    # REMOVE ALL MATCHES
    newLis1 = [x for x in list1 if x not in list2]
    newLis2 = [x for x in list2 if x not in list1]

    pairs = zip(newLis1, newLis2)

    # COMPARE LISTS
    diff_keys = [(x, y) for x, y in pairs if x != y]

    # CREATE OUTPUTLIST
    resultList = createOutput(diff_keys)

    # date = datetime.now
    # check = CompBase(left_name="left",
    #                  right_name="right",
    #                  comp_date=date)

    # print(check)

    class Comp(object):
        pass

    a = Comp()

    a.left_name = files[0].filename
    a.right_name = files[1].filename
    a.comp_date = datetime.now
    compId = db_comp.create_comp(db, a)
    # print(compId)

    class Trans(object):
        pass

    b = Trans()
    new_list = []
    for rec in resultList:
        # print(rec)
        b.trans_id = rec['trans_id']
        b.comp_id = compId
        b.diff_type = rec['diff_type']
        b.value_left = rec['value_left']
        b.value_right = rec['value_right']
        new_list.append(b)
        # recordId = db_transaction.create_transaction(db, b)
    res = db_transaction.bulk_insert(db, new_list)
    return resultList
