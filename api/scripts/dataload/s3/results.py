import re
import json
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
from decimal import Decimal
from datetime import date
import csv
import os
import boto3

from main import app
from app.models import Race, Track, Course
from app.db import db

from app.service_objects.dataload import ResultLoaderWrapper

import code

start_time = time.time()
app_mode = os.environ.get('ENVIRONMENT')


s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
                    aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
bucket = s3.Bucket(os.environ.get('S3_RACE_DATA_BUCKET'))

directory = "./scripts/dataload/s3/"

track_name_regex = r"^[A-z]+"
race_date_regex = r"[0-9]+"
file_regex = r"incoming\/.*\.chart$"

keys = [obj.key for obj in bucket.objects.all() if re.search(file_regex, obj.key)]
files = []

for key in keys:
    fname = key.replace('incoming/', '')
    track = re.search(track_name_regex, fname)
    date = re.search(race_date_regex, fname)
    td = ''.join([track.group(), date.group()])

    file = f"{directory}{key}"
    files.append(file)
    bucket.download_file(key, file)
    bucket.copy({
        'Bucket': os.environ.get('S3_RACE_DATA_BUCKET'),
        'Key': key
    }, key.replace('incoming', f"archive/{date.group()[2:]}/results"))
    loader = ResultLoaderWrapper(
        td,
        file
    )
    loader.load_files()
    if app_mode == 'prod':
        bucket.delete_objects(Delete={'Objects': [{'Key': key}]})

    os.remove(file)

print(f"Total run complete in {round(time.time() - start_time, 2)} seconds")
