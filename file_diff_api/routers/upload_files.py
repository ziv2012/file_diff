from collections import defaultdict
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import false, true
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import List, Tuple
import csv
from io import StringIO
from operator import itemgetter
from datetime import datetime
# from .schemas import CompBase, CompDisplay, TransactionBase, TransactionDisplay
from db import db_comp, db_transaction
from dataclasses import dataclass
from enum import Enum
router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


class DiffType(str):
    ONLY_LEFT = "ONLY_LEFT"
    ONLY_RIGHT = "ONLY_RIGHT"
    # AMOUNT = "AMOUNT"
    # CURRENCY = "CURRENCY"
    # DATE = "DATE"


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


async def readCSV(file: UploadFile):
    dict = defaultdict()
    contents = await file.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict[key] = rows
    buffer.close()


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


@router.post('')
async def upload(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    input_file1 = files[0]
    input_file2 = files[1]
    dict1 = defaultdict()
    contents = await input_file1.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict1[key] = rows
    buffer.close()
    dict2 = defaultdict()
    contents = await input_file2.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict2[key] = rows
    buffer.close()

    # dict1 = await readCSV(files[0])
    # dict2 = await readCSV(files[1])
    # print(dict2)

    # whatever(dict1, dict2)

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
                # resultList.append({"id": rows[0]['id'], "diffType": x, "leftVal": left.get(
                #     x), "rightVal": right.get(x)})

    class Comp(object):
        pass

    a = Comp()

    a.left_name = input_file1.filename
    a.right_name = input_file2.filename
    a.comp_date = datetime.now
    compId = db_comp.create_comp(db, a)
    print(compId)

    class Trans(object):
        pass

    b = Trans()

    for rec in resultList:
        print(rec)
        b.trans_id = rec['trans_id']
        b.comp_id = compId
        b.diff_type = rec['diff_type']
        b.value_left = rec['value_left']
        b.value_right = rec['value_right']
        recordId = db_transaction.create_transaction(db, b)

    return resultList
