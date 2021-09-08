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
import sys

from main import app
from app.models import Race, Track, Course
from app.db import db

from app.service_objects.dataload import RaceDayLoader

import code

BANNED_TRACKS = ['Bc_', 'Spl']


def process_td(td, td_keys):
    files = []
    to_delete = []
    for td_key in td_keys:
        process_flag = True
        file = f"{directory}{td_key}"
        files.append(file)
        bucket.download_file(td_key, file)
        bucket.copy({
            'Bucket': os.environ.get('S3_RACE_DATA_BUCKET'),
            'Key': td_key
        }, td_key.replace('incoming', f"archive/{td[3:9]}"))
        to_delete.append({'Key': td_key})

    if td[0:3] in BANNED_TRACKS:
        print(f"{track} is banned.... skipping")
        process_flag = False

    # dont process if needed files not found
    for f in [f"{directory}incoming/{td}.cr",
              f"{directory}incoming/{td}.ch",
              f"{directory}incoming/{td}.chr",
              f"{directory}incoming/{td}.pgh",
              ]:
        if f not in files:
            process_flag = False

    if process_flag:
        loader = RaceDayLoader(
            td,
            f"{directory}incoming/{td}.cr",
            f"{directory}incoming/{td}.ch",
            f"{directory}incoming/{td}.pgh",
            f"{directory}incoming/{td}.chr"
        )
        loader.load_files()
    else:
        print(f"Archiving and skipping {td}")

    if app_mode == 'prod':
        # print(f"td: {td}, deleting keys: {to_delete}")
        bucket.delete_objects(Delete={'Objects': to_delete})

    for f in files:
        os.remove(f)


s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
                    aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
bucket = s3.Bucket(os.environ.get('S3_RACE_DATA_BUCKET'))
if len(sys.argv) == 3:
    start = sys.argv[1]
    end = sys.argv[2]
else:
    start = 'A'
    end = 'z'

file_regex = rf"incoming\/[{start}-{end}]{{1}}.*\."

app_mode = os.environ.get('ENVIRONMENT')


start_time = time.time()
track_dates = {}
directory = "./scripts/dataload/s3/"

keys = [obj.key for obj in bucket.objects.all() if re.search(file_regex, obj.key)]
files = []

for key in keys:
    if key.endswith('.chart'):
        continue
    fname = key.replace('incoming/', '')
    track = fname[0:3]
    date = fname[3:9]
    td = ''.join([track, date])
    if td in track_dates.keys():
        track_dates[td].append(key)
    else:
        track_dates[td] = [key]


for td, td_keys in track_dates.items():
    process_td(td, td_keys)


print(f"Total run complete in {round(time.time() - start_time, 2)} seconds")
