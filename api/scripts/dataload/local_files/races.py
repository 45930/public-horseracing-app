'''
This file loads the .cr file from DRF, and creates db record for tracks and races.
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
from app.models import Race, Track, Course
from app.db import db

import code

RACE_DATA_TYPE = 'race_file'
race_schema = json.load(open('./file_definitions.json'))[RACE_DATA_TYPE]


def load_races():
    files = [f for f in glob(
        f"./sample_data/even more/*{race_schema['extension']}")]
    #     f"./sample_data/*.drf2_final/out*/exact/*{race_schema['extension']}")]
    # files.extend([f for f in glob(
    #     f"./sample_data/more/*{race_schema['extension']}")])
    # executor = ThreadPoolExecutor(max_workers=4)
    # executor.map(process_file, files)
    # executor.shutdown(wait=True)
    for file in files:
        process_file(file)


def process_file(f):
    with open(f) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        races = {}
        tracks = {}
        courses = {}
        for line in lines:
            line_data = get_line_data(line)
            track_code = line_data['track_code']
            course_key = '-'.join([
                line_data['track_code'],
                str(line_data['distance']),
                line_data['surface_code']
            ])
            race_key = '-'.join([
                course_key,
                str(line_data['date']),
                str(line_data['race_number'])
            ])
            if not track_code in tracks.keys():
                tracks[track_code] = {
                    'code': track_code,
                    'name': line_data['track_name'],
                    'state': line_data['state']
                }
            if not course_key in courses.keys():
                courses[course_key] = {
                    'track_code': line_data['track_code'],
                    'distance': line_data['distance'],
                    'surface': line_data['surface_code']
                }
            if not race_key in races.keys():
                races[race_key] = {
                    'track_code': track_code,
                    'date': line_data['date'],
                    'race_number': line_data['race_number'],
                    'is_state_bred': line_data['state_bred'],
                    'sex_restrictions': line_data['sex_restrictions'],
                    'age_restrictions': line_data['age_restrictions'],
                    'classification': line_data['race_class'],
                    'purse': line_data['purse'],
                    'claim_price': line_data['high_claim_price'],
                    'grade': line_data['grade'],
                    'day_of_week': line_data['day_of_week'],
                    'course_key': course_key
                }

        for track in tracks.values():
            t = Track().find_or_create_by(**{'code': track['code']})
            track['id'] = t.id
            t.update({
                'name': line_data['track_name'],
                'state': line_data['state']
            })

        for course in courses.values():
            course['track_id'] = tracks[course['track_code']]['id']
            c = Course().find_or_create_by(**course)
            course['id'] = c.id

        for race in races.values():
            race['track_id'] = tracks[race['track_code']]['id']
            race['course_id'] = courses[race['course_key']]['id']
            r = Race().find_or_create_by(**({key: race[key] for key in [
                'track_id',
                'course_id',
                'date',
                'race_number'
            ]}))
            copy = race.copy()
            del copy['track_code']
            del copy['course_key']
            r.update(copy)


def get_line_data(line):
    line_data = {}
    for col in race_schema['columns']:
        val = line[col['index']]
        data_type = col['data_type']
        if data_type.startswith('String'):
            line_data[col['name']] = val.lower()
        elif data_type.startswith('DECIMAL'):
            try:
                line_data[col['name']] = Decimal(
                    re.sub('[^0-9.-]', '', val))
            except:
                None
        elif data_type.startswith('Integer'):
            try:
                line_data[col['name']] = int(re.sub('[^0-9]', '', val))
            except:
                None
        elif data_type.startswith('Date'):
            try:
                y = int(val[6:10])
                m = int(val[0:2])
                d = int(val[3:5])
                line_data[col['name']] = date(y, m, d)
            except:
                None
    return line_data


# def process_line(line):
#     line_data = {}
#     for col in race_schema['columns']:
#         val = line[col['index']]
#         data_type = col['data_type']
#         if data_type.startswith('String'):
#             line_data[col['name']] = val.lower()
#         elif data_type.startswith('DECIMAL'):
#             try:
#                 line_data[col['name']] = Decimal(re.sub('[^0-9.-]', '', val))
#             except:
#                 None
#         elif data_type.startswith('Integer'):
#             try:
#                 line_data[col['name']] = int(re.sub('[^0-9]', '', val))
#             except:
#                 None
#         elif data_type.startswith('Date'):
#             try:
#                 y = int(val[6:10])
#                 m = int(val[0:2])
#                 d = int(val[3:5])
#                 line_data[col['name']] = date(y, m, d)
#             except:
#                 None

#     track_data = {
#         'code': line_data['track_code'],
#     }
#     track = Track().find_or_create_by(**track_data)
#     track.update({
#         'name': line_data['track_name'],
#         'state': line_data['state']
#     })

#     course_data = {
#         'track_id': track.id,
#         'track_code': line_data['track_code'],
#         'distance': line_data['distance'],
#         'surface': line_data['surface_code']
#     }
#     course = Course().find_or_create_by(**course_data)

#     race_data = {
#         'track_id': track.id,
#         'course_id': course.id,
#         'date': line_data['date'],
#         'race_number': line_data['race_number']
#     }
#     race = Race().find_or_create_by(**race_data)

#     # find on track_code and update on track.id so that if a race is created by a horse record, we can still find it
#     race.update({
#         'is_state_bred': line_data['state_bred'],
#         'sex_restrictions': line_data['sex_restrictions'],
#         'age_restrictions': line_data['age_restrictions'],
#         'classification': line_data['race_class'],
#         'purse': line_data['purse'],
#         'claim_price': line_data['high_claim_price'],
#         'grade': line_data['grade'],
#         'day_of_week': line_data['day_of_week']
#     }, commit=True)


start_time = time.time()
load_races()
print("--- %s seconds ---" % (time.time() - start_time))
