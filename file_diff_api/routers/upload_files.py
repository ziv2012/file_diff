from collections import defaultdict
from fastapi import APIRouter, Depends, UploadFile, File
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import List
import csv
from io import StringIO
from operator import itemgetter
from datetime import datetime
from db import db_comp, db_transaction
from routers.schemas import TransactionBase


router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


class DiffType(str):
    ONLY_LEFT = "ONLY_LEFT"
    ONLY_RIGHT = "ONLY_RIGHT"


class Comp(object):
    pass


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


def getDiscrepancies(list1: List, list2: List):
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
    return resultList


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
    # GET DISCREPANCIES BETWEEN THE FILES AND CREATE OUTPUT RESULT
    resultList = getDiscrepancies(list1, list2)

    # CREATE NEW COMPARISON
    a = Comp()
    a.left_name = files[0].filename
    a.right_name = files[1].filename
    a.comp_date = datetime.now
    compId = db_comp.create_comp(db, a)

    # INSERT TRANSACTIONS TO DB
    new_list = []
    for rec in resultList:
        b = TransactionBase(
            trans_id=rec['trans_id'],
            comp_id=compId,
            diff_type=rec['diff_type'],
            value_left=rec['value_left'],
            value_right=rec['value_right'],
        )
        new_list.append(b)

    res = db_transaction.bulk_insert(db, new_list)
    return resultList
