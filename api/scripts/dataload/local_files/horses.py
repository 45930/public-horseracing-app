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

FILE_TYPE = 'horse_file'
SCHEMA = json.load(open('./file_definitions.json'))[FILE_TYPE]


def load_data():
    files = [f for f in glob(
        f"./sample_data/even more/*{SCHEMA['extension']}")]
    #     f"./sample_data/*.drf2_final/out*/exact/*{SCHEMA['extension']}")]
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
        horses = {}
        jockeys = {}
        trainers = {}
        owners = {}
        tracks = {}
        results = {}
        for line in lines:
            line_data = get_line_data(line)
            jockeys[line_data['jockey']] = {'full_name': line_data['jockey']}
            trainers[line_data['trainer']] = {
                'full_name': line_data['trainer']}
            owners[line_data['owner']] = {'full_name': line_data['owner']}
            tracks[line_data['track_code']] = {'code': line_data['track_code']}
            results_key = '-'.join([
                line_data['track_code'],
                str(line_data['race_number']),
                str(line_data['date']),
                line_data['name']
            ])
            if not line_data['name'] in horses.keys():
                horses[line_data['name']] = {
                    'name': line_data['name'],
                    'sex': line_data['sex'],
                    'year_born': line_data['year_born'],
                    'month_born': line_data['month_born'],
                    'location_born': line_data['location_born'],
                    'breeder': line_data['breeder'],
                    'color': line_data['color'],
                    'sire': line_data['sire'],
                    'sire_sire': line_data['sire_sire'],
                    'dam': line_data['dam'],
                    'dam_sire': line_data['dam_sire'],
                    'sale_location': line_data['sale_location'],
                    'sale_year': line_data['sale_year'],
                    'sale_price': line_data['sale_price'],
                    'stud_fee': line_data['stud_fee']
                }
            if not results_key in results.keys():
                results[results_key] = {
                    'track': line_data['track_code'],
                    'date': line_data['date'],
                    'race_number': line_data['race_number'],
                    'name': line_data['name'],
                    'trainer': line_data['trainer'],
                    'jockey': line_data['jockey'],
                    'owner': line_data['owner'],
                    'last_raced': line_data['last_raced'],
                    'lasix': line_data['lasix'],
                    'claiming_price': line_data['claiming_price'],
                    'lifetime_earn': line_data['lifetime_earn'],
                    'lifetime_starts': line_data['lifetime_starts'],
                    'lifetime_wins': line_data['lifetime_wins'],
                    'lifetime_places': line_data['lifetime_places'],
                    'lifetime_shows': line_data['lifetime_shows'],
                    'turf_earn': line_data['turf_earn'],
                    'turf_starts': line_data['turf_starts'],
                    'turf_wins': line_data['turf_wins'],
                    'turf_places': line_data['turf_places'],
                    'turf_shows': line_data['turf_shows']
                }

        for track in tracks.values():
            t = Track().find_or_create_by(**{'code': track['code']})
            track['id'] = t.id

        for jockey in jockeys.values():
            j = Jockey().find_or_create_by(
                **{'full_name': jockey['full_name']})
            jockey['id'] = j.id

        for trainer in trainers.values():
            t = Trainer().find_or_create_by(
                **{'full_name': trainer['full_name']})
            trainer['id'] = t.id

        for owner in owners.values():
            o = Owner().find_or_create_by(
                **{'full_name': owner['full_name']})
            owner['id'] = o.id

        for horse in horses.values():
            h = Horse().find_or_create_by(
                **{'name': horse['name']})
            h.update(horse)
            horse['id'] = h.id

        for result in results.values():
            race_data = {
                'track_id': tracks[result['track']]['id'],
                'date': result['date'],
                'race_number': result['race_number']
            }
            race = Race().find_or_create_by(**race_data)
            res = Result().find_or_create_by(**{
                'race_id': race.id,
                'horse_id': horses[result['name']]['id']
            })
            copy = result.copy()
            copy['jockey_id'] = jockeys[copy['jockey']]['id']
            copy['trainer_id'] = trainers[copy['trainer']]['id']
            copy['owner_id'] = owners[copy['owner']]['id']
            del copy['track']
            del copy['date']
            del copy['race_number']
            del copy['name']
            del copy['trainer']
            del copy['jockey']
            del copy['owner']
            res.update(copy)


def get_line_data(line):
    line_data = {}
    for col in SCHEMA['columns']:
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
    return line_data


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

    horse_data = {
        'name': line_data['name']
    }
    horse = Horse().find_by_or_create_by(**horse_data)
    horse.update({
        'sex': line_data['sex'],
        'year_born': line_data['year_born'],
        'month_born': line_data['month_born'],
        'location_born': line_data['location_born'],
        'breeder': line_data['breeder'],
        'color': line_data['color'],
        'sire': line_data['sire'],
        'sire_sire': line_data['sire_sire'],
        'dam': line_data['dam'],
        'dam_sire': line_data['dam_sire'],
        'sale_location': line_data['sale_location'],
        'sale_year': line_data['sale_year'],
        'sale_price': line_data['sale_price'],
        'stud_fee': line_data['stud_fee']
    })

    trainer = Trainer().find_or_create_by(full_name=line_data['trainer'])
    jockey = Jockey().find_or_create_by(full_name=line_data['jockey'])
    owner = Owner().find_or_create_by(full_name=line_data['owner'])

    track_data = {
        'code': line_data['track_code'],
    }
    track = Track().find_or_create_by(**track_data)

    race_data = {
        'track_id': track.id,
        'date': line_data['date'],
        'race_number': line_data['race_number']
    }
    race = Race().find_or_create_by(**race_data)

    result = Result().find_or_create_by(
        race_id=race.id,
        horse_id=horse.id
    )
    result.update({
        'trainer_id': trainer.id,
        'jockey_id': jockey.id,
        'owner_id': owner.id,
        'last_raced': line_data['last_raced'],
        'lasix': line_data['lasix'],
        'claiming_price': line_data['claiming_price'],
        'lifetime_earn': line_data['lifetime_earn'],
        'lifetime_starts': line_data['lifetime_starts'],
        'lifetime_wins': line_data['lifetime_wins'],
        'lifetime_places': line_data['lifetime_places'],
        'lifetime_shows': line_data['lifetime_shows'],
        'turf_earn': line_data['turf_earn'],
        'turf_starts': line_data['turf_starts'],
        'turf_wins': line_data['turf_wins'],
        'turf_places': line_data['turf_places'],
        'turf_shows': line_data['turf_shows']
    })


start_time = time.time()
load_data()
print("--- %s seconds ---" % (time.time() - start_time))
