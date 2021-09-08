import re
import json
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
from decimal import Decimal
from datetime import date
from glob import glob
import csv
import os
import boto3
import sys
import subprocess
import zipfile

from main import app
from app.models import Race, Track, Course
from app.db import db

from app.service_objects.dataload import DrfFileDownloader

import code

DrfFileDownloader().download_url()
with zipfile.ZipFile('./output.zip', 'r') as zip_ref:
    zip_ref.extractall('./output')

s3_client = boto3.client('s3',
                         aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
                         aws_secret_access_key=os.environ.get('S3_SECRET_KEY')
                         )
for filename in glob('./output/*'):

    if filename in ['.', '..', '.keep']:
        continue
    else:
        s3_client.upload_file(
            filename,
            os.environ.get('S3_RACE_DATA_BUCKET'),
            f'incoming/{os.path.basename(filename)}'
        )
