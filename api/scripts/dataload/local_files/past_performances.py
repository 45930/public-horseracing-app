'''
This file loads the .chr file from DRF, and creates db record for past performances
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
from app.models import Horse, PastPerformance
from app.db import db

import code

FILE_TYPE = 'past_performance_file'
SCHEMA = json.load(open('./file_definitions.json'))[FILE_TYPE]


def load_data():
    files = [f for f in glob(
        f"./sample_data/even more/*{SCHEMA['extension']}")]
    #     f"./sample_data/*.drf2_final/out*/exact/*{SCHEMA['extension']}")]
    # files.extend([f for f in glob(
    #     f"./sample_data/more/*{SCHEMA['extension']}")])
    # executor = ThreadPoolExecutor(max_workers=4)
    # executor.map(process_file, files)
    # executor.shutdown(wait=True)
    for file in files:
        if ('Bel' in file) or ('Cd_' in file) or ('Sa_' in file):
            process_file(file)


def process_file(f):
    with open(f) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        for line in lines:
            process_line(line)


def process_line(line):
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

    try:
        horse_data = {
            'name': line_data['horse_name']
        }

        horse = Horse().find_by(**horse_data)

        past_performance_data = {
            'horse_id': horse.id,
            'track_code': line_data['track_code'],
            'race_date': line_data['race_date'],
        }

        past_performance = PastPerformance().create(**past_performance_data)
        past_performance.update({
            'today_track': line_data['today_track'],
            'today_date': line_data['today_date'],
            'today_race_number': line_data['today_race_number'],
            'horse_name': line_data['horse_name'],
            'foreign_or_domestic': line_data['foreign_or_domestic'],
            'foreign_race': line_data['foreign_race'],
            'race_number': line_data['race_number'],
            'surface': line_data['surface'],
            'timeform_code': line_data['timeform_code'],
            'inner_track_code': line_data['inner_track_code'],
            'distance': line_data['distance'],
            'race_class': line_data['race_class'],
            'claim_price': line_data['claim_price'],
            'purse': line_data['purse'],
            'track_condition': line_data['track_condition'],
            'sex_restrictions': line_data['sex_restrictions'],
            'age_restrictions': line_data['age_restrictions'],
            'state_bred': line_data['state_bred'],
            'field_size': line_data['field_size'],
            'first_fraction': line_data['first_fraction'],
            'second_fraction': line_data['second_fraction'],
            'third_fraction': line_data['third_fraction'],
            'fourth_fraction': line_data['fourth_fraction'],
            'fifth_fraction': line_data['fifth_fraction'],
            'sixth_fraction': line_data['sixth_fraction'],
            'final_time': line_data['final_time'],
            'first_horse': line_data['first_horse'],
            'second_horse': line_data['second_horse'],
            'third_horse': line_data['third_horse'],
            'grade': line_data['grade'],
            'post_position': line_data['post_position'],
            'first_call_position': line_data['first_call_position'],
            'first_call_lengths_back': line_data['first_call_lengths_back'],
            'first_call_position': line_data['first_call_position'],
            'first_call_lengths_back': line_data['first_call_lengths_back'],
            'first_call_position': line_data['first_call_position'],
            'first_call_lengths_back': line_data['first_call_lengths_back'],
            'second_call_position': line_data['second_call_position'],
            'second_call_lengths_back': line_data['second_call_lengths_back'],
            'third_call_position': line_data['third_call_position'],
            'third_call_lengths_back': line_data['third_call_lengths_back'],
            'fourth_call_position': line_data['fourth_call_position'],
            'fourth_call_lengths_back': line_data['fourth_call_lengths_back'],
            'stretch_call_position': line_data['stretch_call_position'],
            'stretch_call_lengths_back': line_data['stretch_call_lengths_back'],
            'final_call_position': line_data['final_call_position'],
            'final_call_lengths_back': line_data['final_call_lengths_back'],
            'beyer_or_foreign_speed': line_data['beyer_or_foreign_speed'],
            'odds': line_data['odds'],
            'odds_position': line_data['odds_position'],
            'claimed_code': line_data['claimed_code'],
            'lasix': line_data['lasix'],
            'bute': line_data['bute'],
            'blinkers': line_data['blinkers'],
            'bandages': line_data['bandages'],
            'jockey': line_data['jockey'],
            'trainer': line_data['trainer'],
            'track_variant': line_data['track_variant'],
            'speed_rating': line_data['speed_rating'],
            'breed': line_data['breed'],
            'owner': line_data['owner']
        })

    except:
        import code
        code.interact(local=dict(globals(), **locals()))


start_time = time.time()
load_data()
print("--- %s seconds ---" % (time.time() - start_time))
