'''
This file loads the .ch file from DRF, and creates db record for horses, trainers, owners, jockeys, and results
It will create races if thee reaces for which a horse is entered does not exist.
'''

import re
import json
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
from decimal import Decimal
from datetime import date
import csv

from main import app
from app.models import Horse, Trainer, Owner, Jockey, Race, Result, Track
from app.db import db

import code

FILE_TYPE = 'results_file'
SCHEMA = json.load(open('./file_definitions.json'))[FILE_TYPE]


def load_data():
    files = [f for f in glob(
        f"./sample_data/even more/*{SCHEMA['extension']}")]
    #     f"./sample_data/results/*{SCHEMA['extension']}")]
    # files.extend([f for f in glob(
    #     f"./sample_data/more/*{SCHEMA['extension']}")])
    executor = ThreadPoolExecutor(max_workers=4)
    executor.map(process_file, files)
    executor.shutdown(wait=True)
    # for file in files:
    #     process_file(file)


def process_file(f):
    with open(f) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        headers = next(lines)
        track_code = headers[2].replace(' ', '').lower()
        race_date = headers[3]
        y = int(race_date[0:4])
        m = int(race_date[4:6])
        d = int(race_date[6:8])

        try:
            race_date = date(y, m, d)
        except:
            import code
            code.interact(local=dict(globals(), **locals()))

        for line in lines:
            if line[0] == 'S':
                process_starter(line, track_code, race_date)


def process_starter(line, track_code, race_date):
    line_data = {}
    for col in SCHEMA['columns']:
        val = line[col['index']]
        data_type = col['data_type']
        if data_type.startswith('String'):
            line_data[col['name']] = val.lower()
        elif data_type.startswith('DECIMAL'):
            try:
                line_data[col['name']] = Decimal(re.sub('[^0-9.-]', '', val))
            except:
                line_data[col['name']] = None
        elif data_type.startswith('Integer'):
            try:
                line_data[col['name']] = int(re.sub('[^0-9]', '', val))
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

    horse_data = {
        'name': re.sub('\s\(([^)]+)\)', '', line_data['horse_name'])
    }
    horse = Horse().find_or_create_by(**horse_data)

    track_data = {
        'code': track_code,
    }
    track = Track().find_or_create_by(**track_data)

    race_data = {
        'track_id': track.id,
        'date': race_date,
        'race_number': line_data['race_number']
    }
    race = Race().find_or_create_by(**race_data)

    result = Result().find_or_create_by(
        race_id=race.id,
        horse_id=horse.id
    )
    result.update({
        'odds': line_data['odds'],
        'post_position': line_data['post_position'],
        'program_number': line_data['program_number'],
        'start_position': line_data['start_position'],
        'first_call_position': line_data['first_call_position'],
        'second_call_position': line_data['second_call_position'],
        'third_call_position': line_data['third_call_position'],
        'fourth_call_position': line_data['fourth_call_position'],
        'fifth_call_position': line_data['fifth_call_position'],
        'final_position': line_data['final_position'],
        'first_call_lengths_ahead': line_data['first_call_lengths_ahead'],
        'second_call_lengths_ahead': line_data['second_call_lengths_ahead'],
        'third_call_lengths_ahead': line_data['third_call_lengths_ahead'],
        'fourth_call_lengths_ahead': line_data['fourth_call_lengths_ahead'],
        'fifth_call_lengths_ahead': line_data['fifth_call_lengths_ahead'],
        'final_lengths_ahead': line_data['final_lengths_ahead'],
        'first_call_lengths_behind': line_data['first_call_lengths_behind'],
        'second_call_lengths_behind': line_data['second_call_lengths_behind'],
        'third_call_lengths_behind': line_data['third_call_lengths_behind'],
        'fifth_call_lengths_behind': line_data['fifth_call_lengths_behind'],
        'final_lengths_behind': line_data['final_lengths_behind'],
        'win_pay': line_data['win_pay'],
        'place_pay': line_data['place_pay'],
        'show_pay': line_data['show_pay']
    })


start_time = time.time()
load_data()
print("--- %s seconds ---" % (time.time() - start_time))
