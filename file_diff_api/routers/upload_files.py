from fastapi import APIRouter, Depends, UploadFile, File
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import List
import csv
from io import StringIO

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
        print(rows)

    # pairs = zip(list1, list2)

    # diff_keys = [[k for k in x if x[k] != y[k]] for x, y in pairs if x != y]
    return list2
