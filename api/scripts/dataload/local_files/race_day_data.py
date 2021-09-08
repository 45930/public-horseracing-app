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
from app.models import Horse, Trainer, Owner, Jockey, Race, Result, Track, Course, PastPerformance
from app.db import db

import code

RACE_DATA_TYPE = 'race_file'
race_schema = json.load(open('./file_definitions.json'))[RACE_DATA_TYPE]
race_file_ext = race_schema['extension']

HORSE_DATA_TYPE = 'horse_file'
horse_schema = json.load(open('./file_definitions.json'))[HORSE_DATA_TYPE]
horse_file_ext = horse_schema['extension']

PAST_PERFORMANCE_DATA_TYPE = 'past_performance_file'
past_performance_schema = json.load(
    open('./file_definitions.json'))[PAST_PERFORMANCE_DATA_TYPE]
past_performance_file_ext = past_performance_schema['extension']


def load_data():
    # files = [f for f in glob(
    #     f"./sample_data/more/*")]
    files = [f for f in glob(
        f"./sample_data/more/Cd_200516*")]
    track_dates = set()
    for f in files:
        fname = os.path.basename(f)
        track = fname[0:3].lower()
        date = fname[3:9]
        track_dates.add(''.join([track, date]))
    for td in track_dates:
        print(f"processing {td}")
        race_file = f"./sample_data/more/{td}{race_file_ext}"
        horse_file = f"./sample_data/more/{td}{horse_file_ext}"
        past_performance_file = f"./sample_data/more/{td}{past_performance_file_ext}"
        tracks, courses, races = load_races(race_file)
        trainers, jockeys, owners, horses, results = load_horses(
            horse_file, races)
        past_performances = load_past_performances(
            past_performance_file, horses)


def load_races(race_file):
    with open(race_file) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        races = {}
        tracks = {}
        courses = {}
        for line in lines:
            line_data = get_line_data(line, race_schema)
            track_code = line_data['track_code']
            course_key = '-'.join([
                line_data['track_code'],
                str(line_data['distance']),
                line_data['surface_code']
            ])
            race_key = '-'.join([
                line_data['track_code'],
                str(line_data['date']),
                str(line_data['race_number'])
            ])
            tracks[track_code] = {
                'code': track_code,
                'name': line_data['track_name'],
                'state': line_data['state']
            }

            courses[course_key] = {
                'track_code': line_data['track_code'],
                'distance': line_data['distance'],
                'surface': line_data['surface_code']
            }

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

        races_to_add = []
        races_to_update = []
        for race in races.values():
            race['track_id'] = tracks[race['track_code']]['id']
            race['course_id'] = courses[race['course_key']]['id']
            r = Race().find_by(**({key: race[key] for key in [
                'track_id',
                'date',
                'race_number'
            ]}))
            copy = race.copy()
            del copy['track_code']
            del copy['course_key']
            if r:
                existing = r.as_dict()
                new = Race(**copy).as_dict()
                new['id'] = existing['id']
                race['id'] = r.id
                if existing == new:
                    # No change
                    pass
                else:
                    races_to_update.append(copy)
            else:
                races_to_add.append(Race(**copy))

        ids_to_update = set(map(lambda race: race['id'], races_to_update))
        if len(ids_to_update) > 0:
            print(f"updating races: {ids_to_update}")
        for race in races_to_update:
            r = Race().find(race['id']).update(race)

        try:
            db.session.add_all(races_to_add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding races: {e}")
            for r in races_to_add:
                try:
                    db.session.add(r)
                    db.session.commit()
                except:
                    db.session.rollback()

    return tracks, courses, races


def load_horses(horse_file, races):
    with open(horse_file) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        horses = {}
        jockeys = {}
        trainers = {}
        owners = {}
        tracks = {}
        results = {}
        for line in lines:
            line_data = get_line_data(line, horse_schema)
            jockeys[line_data['jockey']] = {'full_name': line_data['jockey']}
            trainers[line_data['trainer']] = {
                'full_name': line_data['trainer']}
            owners[line_data['owner']] = {'full_name': line_data['owner']}
            tracks[line_data['track_code']] = {'code': line_data['track_code']}
            race_key = '-'.join([
                line_data['track_code'],
                str(line_data['date']),
                str(line_data['race_number'])
            ])
            results_key = '-'.join([
                line_data['track_code'],
                str(line_data['race_number']),
                str(line_data['date']),
                line_data['name']
            ])
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

        horses_to_update = []
        horses_to_add = []
        for horse in horses.values():
            h = Horse().find_by(
                **{'name': horse['name']})
            if h:
                existing = h.as_dict()
                new = Horse(**horse).as_dict()
                new['id'] = existing['id']
                horse['id'] = h.id
                if existing == new:
                    # No change
                    pass
                else:
                    horses_to_update.append(horse)
            else:
                horses_to_add.append(Horse(**horse))

        ids_to_update = set(map(lambda horse: horse['id'], horses_to_update))
        if len(ids_to_update) > 0:
            print(f"updating horses: {ids_to_update}")
        for horse in horses_to_update:
            h = Horse().find(horse['id']).update(horse)

        try:
            db.session.add_all(horses_to_add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding horses: {e}")
            for h in horses_to_add:
                try:
                    db.session.add(h)
                    db.session.commit()
                except:
                    db.session.rollback()

        results_to_update = []
        results_to_add = []
        for result in results.values():
            race = races[race_key]
            if 'id' not in race.keys():
                # race was created above and we don't know the id yet
                race_id = Race().find_by(**{
                    'track_id': tracks[race['track_code']]['id'],
                    'date': race['date'],
                    'race_number': race['race_number']
                }).id
                race['id'] = race_id
            horse = horses[result['name']]
            if 'id' not in horse.keys():
                # horse was created above and we don't know the id yet
                horse_id = Horse().find_by(**{
                    'name': result['name']
                }).id
                horse['id'] = horse_id
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
            res = Result().find_by(**{
                'race_id': races[race_key]['id'],
                'horse_id': horses[result['name']]['id']
            })
            if res:
                existing = res.as_dict()
                new = Result(**copy).as_dict()
                existing = {key: existing[key]
                            for key in copy.keys() if key in existing.keys()}
                new = {key: new[key] for key in existing.keys()}
                result['id'] = res.id
                if existing == new:
                    # No change
                    pass
                else:
                    results_to_update.append(copy)
            else:
                results_to_add.append(Result(**copy))
        ids_to_update = set(
            map(lambda result: result['id'], results_to_update))
        if len(ids_to_update) > 0:
            print(f"updating results: {ids_to_update}")
        for result in results_to_update:
            res = Result().find(result['id']).update(result)

        try:
            db.session.add_all(results_to_add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding results: {e}")
            for res in results_to_add:
                try:
                    db.session.add(res)
                    db.session.commit()
                except:
                    db.session.rollback()
    return trainers, jockeys, owners, horses, results


def load_past_performances(past_performance_file, horses):
    with open(past_performance_file) as open_file:
        lines = csv.reader(open_file, delimiter=',', quotechar='"')
        past_performances = {}
        for line in lines:
            line_data = get_line_data(line, past_performance_schema)
            past_performance_key = '-'.join([
                line_data['today_track'],
                str(line_data['today_date']),
                str(line_data['today_race_number']),
                line_data['horse_name'],
                str(line_data['race_date']),
            ])
            if not line_data['horse_name'] in horses.keys():
                h = Horse().find_or_create_by(
                    **{'name': line_data['horse_name']})
                horses[line_data['horse_name']] = {
                    'id': h.id
                }
            past_performances[past_performance_key] = {
                'horse_id': horses[line_data['horse_name']]['id'],
                'track_code': line_data['track_code'],
                'race_date': line_data['race_date'],
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
            }

        past_performances_to_update = []
        past_performances_to_add = []
        for past_performance in past_performances.values():
            pp = PastPerformance().find_by(**{
                'horse_id': past_performance['horse_id'],
                'track_code': past_performance['track_code'],
                'race_date': past_performance['race_date']}
            )
            if pp:
                existing = pp.as_dict()
                new = PastPerformance(**past_performance).as_dict()
                new['id'] = existing['id']
                past_performance['id'] = pp.id
                if existing == new:
                    # No change
                    pass
                else:
                    past_performances_to_update.append(past_performance)
            else:
                past_performances_to_add.append(
                    PastPerformance(**past_performance))

        ids_to_update = set(
            map(lambda past_performance: past_performance['id'], past_performances_to_update))
        if len(ids_to_update) > 0:
            print(f"updating past_performances: {ids_to_update}")
        for past_performance in past_performances_to_update:
            pp = PastPerformance().find(
                past_performance['id']).update(past_performance)

        try:
            db.session.add_all(past_performances_to_add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding past_performances: {e}")
            for pp in past_performances_to_add:
                try:
                    db.session.add(pp)
                    db.session.commit()
                except:
                    db.session.rollback()

    return past_performances


def get_line_data(line, type):
    line_data = {}
    for col in type['columns']:
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


start_time = time.time()
load_data()
print("--- %s seconds ---" % (time.time() - start_time))
