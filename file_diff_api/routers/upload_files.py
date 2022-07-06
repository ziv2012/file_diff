from fastapi import APIRouter, Depends, UploadFile, File
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

    for rows in list1:
        rows['date'] = datetime.strptime(
            rows['date'], "%m/%d/%Y").strftime("%Y-%m-%d")

    for rows in list2:
        rows['date'] = datetime.strptime(
            rows['date'], "%m/%d/%Y").strftime("%Y-%m-%d")

    list1, list2 = [sorted(l, key=itemgetter('id'))
                    for l in (list1, list2)]
    pairs = zip(list1, list2)
    diff_keys = [(x, y) for x, y in pairs if x != y]
    return diff_keys
