import re
import json
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
from decimal import Decimal
from datetime import date
import csv
import os

from main import app
from app.db import db

import code


class BaseLoader():
    def __init__(self, file, model_cache, schema):
        self.file = file
        self.model_cache = model_cache
        self.schema = schema

    def load(self):
        with open(self.file) as open_file:
            try:
                lines = self.parse_csv(open_file)
                for line in lines:
                    line_data = self.get_line_data(line)
                    self.insert_file_models(line_data)
            except csv.Error:
                print(f"$ ERROR: Could not strictly parse csv: {self.file}")
                return

        self.create_sql_records()

    def parse_csv(self, open_file):
        return csv.reader(open_file, delimiter=',', quotechar='"', strict=True)

    def get_line_data(self, line, schema=None):
        line_data = {}
        if not schema:
            schema = self.schema
        for col in schema['columns']:
            val = line[col['index']]
            data_type = col['data_type']
            if data_type.startswith('String'):
                line_data[col['name']] = val.lower()
            elif data_type.startswith('DECIMAL'):
                try:
                    line_data[col['name']] = Decimal(
                        re.sub('[^0-9.-]', '', val))
                except:
                    line_data[col['name']] = None
            elif data_type.startswith('Integer'):
                try:
                    line_data[col['name']] = int(val)
                except ValueError:
                    try:
                        line_data[col['name']] = int(float(val))
                    except:
                        line_data[col['name']] = None
            elif data_type.startswith('Date'):
                try:
                    y = int(val[6:10])
                    m = int(val[0:2])
                    d = int(val[3:5])
                    line_data[col['name']] = date(y, m, d)
                except:
                    line_data[col['name']] = None
        return line_data
