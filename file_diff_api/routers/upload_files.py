from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import false, true
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import List
import csv
from io import StringIO
from operator import itemgetter
from datetime import datetime

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


@router.post('')
async def upload(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    input_file1 = files[0]
    input_file2 = files[1]
    dict1 = {}
    contents = await input_file1.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict1[key] = rows

    buffer.close()
    dict2 = {}
    contents = await input_file2.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    for rows in csvReader:
        key = rows['id']
        dict2[key] = rows
    buffer.close()

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
        if rows[0]['id'] != rows[1]['id']:
            resultList.append({"id": rows[0]['id'], "diffType": "onlyLeft"})
            resultList.append({"id": rows[1]['id'], "diffType": "onlyRight"})
        else:
            left, right = rows
            mismatchkeys = {key for key in left.keys(
            ) & right if left[key] != right[key]}
            for x in mismatchkeys:
                resultList.append({"id": rows[0]['id'], "diffType": x, "leftVal": left.get(
                    x), "rightVal": right.get(x)})

    return resultList
