from .base_loader import BaseLoader, csv

from app.models import Jockey, Trainer, Owner, Horse, Result
from app.db import db


class HorseLoader(BaseLoader):
    def __init__(self, horse_file, model_cache, horse_schema, betting_into_file, betting_into_schema):
        self.file = horse_file
        self.model_cache = model_cache
        self.schema = horse_schema
        self.betting_info_file = betting_into_file
        self.betting_into_schema = betting_into_schema

    def load(self):
        with open(self.file) as open_file:
            lines = self.parse_csv(open_file)
            try:
                for line in lines:
                    line_data = self.get_line_data(line)
                    self.insert_file_models(line_data)
            except csv.Error:
                print(f"$ ERROR: Could not strictly parse csv: {self.file}")
                return

        with open(self.betting_info_file) as open_file:
            lines = self.parse_csv(open_file)
            try:
                for line in lines:
                    line_data = self.get_line_data(
                        line, self.betting_into_schema)
                    self.insert_betting_info_models(line_data)
            except csv.Error:
                print(
                    f"$ ERROR: Could not strictly parse csv: {self.betting_info_file}")
                return

        self.create_sql_records()

    def insert_betting_info_models(self, line_data):
        track_code = line_data['track_code']
        race_key = self.model_cache.keygen([
            track_code,
            line_data['date'],
            line_data['race_number']
        ])
        if not self.model_cache.lookup('race_file', race_key):
            # No race found -- probably means this is a Qhorse race.  Dont want to load it
            return

        result_key = self.model_cache.keygen([
            track_code,
            line_data['race_number'],
            line_data['date'],
            line_data['horse_name']
        ])

        result = self.model_cache.lookup('result_file', result_key)
        new_info = {
            'program_number': line_data['betting_number'],
            'morning_line_odds': line_data['morning_line_odds'],
        }

        if not result:
            # this beetting info is for a horse that is not in the race
            pass
        else:
            self.model_cache.insert(
                'result_file',
                result_key,
                {**result, **new_info}
            )

    def insert_file_models(self, line_data):
        track_code = line_data['track_code']
        race_key = self.model_cache.keygen([
            track_code,
            line_data['date'],
            line_data['race_number']
        ])
        if not self.model_cache.lookup('race_file', race_key):
            # No race found -- probably means this is a Qhorse race.  Dont want to load it
            return

        result_key = self.model_cache.keygen([
            track_code,
            line_data['race_number'],
            line_data['date'],
            line_data['name']
        ])
        self.model_cache.insert(
            'jockey_file',
            line_data['jockey'],
            {'full_name': line_data['jockey']}
        )
        self.model_cache.insert(
            'trainer_file',
            line_data['trainer'],
            {'full_name': line_data['trainer']}
        )
        self.model_cache.insert(
            'owner_file',
            line_data['owner'],
            {'full_name': line_data['owner']}
        )
        self.model_cache.insert(
            'horse_file',
            line_data['name'],
            {
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
        )
        self.model_cache.insert(
            'result_file',
            result_key,
            {
                'race_key': race_key,
                'track': line_data['track_code'],
                'date': line_data['date'],
                'race_number': line_data['race_number'],
                'name': line_data['name'],
                'trainer': line_data['trainer'],
                'jockey': line_data['jockey'],
                'owner': line_data['owner'],
                'last_raced': line_data['last_raced'],
                'lasix': line_data['lasix'],
                'post_position': line_data['post_position'],
                'blinker_change': line_data['blinker_change'],
                'claiming_price': line_data['claiming_price'],
                'cur_year_earn': line_data['cur_year_earn'],
                'cur_year_starts': line_data['cur_year_starts'],
                'cur_year_wins': line_data['cur_year_wins'],
                'cur_year_places': line_data['cur_year_places'],
                'cur_year_shows': line_data['cur_year_shows'],
                'prior_year_earn': line_data['prior_year_earn'],
                'prior_year_starts': line_data['prior_year_starts'],
                'prior_year_wins': line_data['prior_year_wins'],
                'prior_year_places': line_data['prior_year_places'],
                'prior_year_shows': line_data['prior_year_shows'],
                'lifetime_earn': line_data['lifetime_earn'],
                'lifetime_starts': line_data['lifetime_starts'],
                'lifetime_wins': line_data['lifetime_wins'],
                'lifetime_places': line_data['lifetime_places'],
                'lifetime_shows': line_data['lifetime_shows'],
                'turf_earn': line_data['turf_earn'],
                'turf_starts': line_data['turf_starts'],
                'turf_wins': line_data['turf_wins'],
                'turf_places': line_data['turf_places'],
                'turf_shows': line_data['turf_shows'],
                'fast_dirt_earn': line_data['fast_dirt_earn'],
                'fast_dirt_starts': line_data['fast_dirt_starts'],
                'fast_dirt_wins': line_data['fast_dirt_wins'],
                'fast_dirt_places': line_data['fast_dirt_places'],
                'fast_dirt_shows': line_data['fast_dirt_shows'],
                'track_earn': line_data['track_earn'],
                'track_starts': line_data['track_starts'],
                'track_wins': line_data['track_wins'],
                'track_places': line_data['track_places'],
                'track_shows': line_data['track_shows'],
                'distance_earn': line_data['distance_earn'],
                'distance_starts': line_data['distance_starts'],
                'distance_wins': line_data['distance_wins'],
                'distance_places': line_data['distance_places'],
                'distance_shows': line_data['distance_shows'],
                'jockey_meet_starts': line_data['jockey_meet_starts'],
                'jockey_meet_earn': line_data['jockey_meet_earn'],
                'jockey_meet_wins': line_data['jockey_meet_wins'],
                'jockey_meet_places': line_data['jockey_meet_places'],
                'jockey_meet_shows': line_data['jockey_meet_shows'],
                'jockey_ytd_starts': line_data['jockey_ytd_starts'],
                'jockey_ytd_earn': line_data['jockey_ytd_earn'],
                'jockey_ytd_wins': line_data['jockey_ytd_wins'],
                'jockey_ytd_places': line_data['jockey_ytd_places'],
                'jockey_ytd_shows': line_data['jockey_ytd_shows'],
                'trainer_meet_starts': line_data['trainer_meet_starts'],
                'trainer_meet_earn': line_data['trainer_meet_earn'],
                'trainer_meet_wins': line_data['trainer_meet_wins'],
                'trainer_meet_places': line_data['trainer_meet_places'],
                'trainer_meet_shows': line_data['trainer_meet_shows'],
                'trainer_ytd_starts': line_data['trainer_ytd_starts'],
                'trainer_ytd_earn': line_data['trainer_ytd_earn'],
                'trainer_ytd_wins': line_data['trainer_ytd_wins'],
                'trainer_ytd_places': line_data['trainer_ytd_places'],
                'trainer_ytd_shows': line_data['trainer_ytd_shows']
            }
        )

    def create_sql_records(self):
        if 'jockey_file' in self.model_cache.cache.keys():
            jockeys = self.model_cache.cache['jockey_file']
        else:
            # No valid races in this file
            return

        for jname, jockey in jockeys.items():
            j = self.model_cache.lookup('jockey_sql', jname)
            if not j:
                j = Jockey().find_or_create_by(
                    **{'full_name': jockey['full_name']})
                self.model_cache.insert('jockey_sql', jname, j)

        trainers = self.model_cache.cache['trainer_file']
        for tname, trainer in trainers.items():
            j = self.model_cache.lookup('trainer_sql', tname)
            if not j:
                t = Trainer().find_or_create_by(
                    **{'full_name': trainer['full_name']})
                self.model_cache.insert('trainer_sql', tname, t)

        owners = self.model_cache.cache['owner_file']
        for oname, owner in owners.items():
            o = self.model_cache.lookup('owner_sql', oname)
            if not o:
                o = Owner().find_or_create_by(
                    **{'full_name': owner['full_name']})
                self.model_cache.insert('owner_sql', oname, o)

        horses_to_add = []
        horses_to_update = []
        horses = self.model_cache.cache['horse_file']
        for hname, horse in horses.items():
            h = self.model_cache.lookup('horse_sql', hname)
            if not h:
                h = Horse().find_by(**{
                    'name': hname,
                    'year_born': horse['year_born'],
                    'location_born': horse['location_born']
                })
                if h:
                    self.model_cache.insert('horse_sql', hname, h)

            copy = horse.copy()
            if h:
                existing = h.as_dict()
                new = Horse(**copy).as_dict()
                new['id'] = existing['id']
                copy['id'] = h.id
                if existing == new:
                    # No change
                    pass
                else:
                    existing = set(existing.items())
                    new = set(new.items())
                    # print(
                    #     f"Updated horse {h.id}: old: {existing - new}, new: {new - existing}")
                    horses_to_update.append(copy)
            else:
                horses_to_add.append(Horse(**copy))

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

        results_to_add = []
        results_to_update = []
        results = self.model_cache.cache['result_file']
        for result_key, result in results.items():
            r = self.model_cache.lookup('result_sql', result_key)
            if not r:
                try:
                    race_id = self.model_cache.lookup(
                        'race_sql', result['race_key']).id
                except:
                    print(f"Race not found {result['race_key']}")
                    continue
                if self.model_cache.lookup(
                        'horse_sql', result['name']):
                    horse_id = self.model_cache.lookup(
                        'horse_sql', result['name']).id
                else:
                    horse_data = self.model_cache.lookup(
                        'horse_file', result['name'])
                    h = Horse().find_by(**{
                        'name': horse_data['name'],
                        'year_born': horse_data['year_born'],
                        'month_born': horse_data['month_born']
                    })
                    horse_id = h.id
                    self.model_cache.insert(
                        'horse_sql', result['name'], h)
                r = Result().find_by(**{
                    'race_id': race_id,
                    'horse_id': horse_id,
                })
                if r:
                    self.model_cache.insert('result_sql', result_key, r)

            copy = {
                k: result[k]
                for k in result.keys() - {
                    'race_key',
                    'track',
                    'date',
                    'race_number',
                    'name',
                    'trainer',
                    'jockey',
                    'owner',
                }
            }
            copy['race_id'] = race_id
            copy['horse_id'] = horse_id
            copy['jockey_id'] = self.model_cache.lookup(
                'jockey_sql', result['jockey']).id
            copy['trainer_id'] = self.model_cache.lookup(
                'trainer_sql', result['trainer']).id
            copy['owner_id'] = self.model_cache.lookup(
                'owner_sql', result['owner']).id

            if r:
                existing = r.as_dict()
                result_id = existing['id']
                new = Result(**copy).as_dict()
                existing = {
                    key: existing[key]
                    for key in new.keys() if key in existing.keys()
                }
                new = {key: new[key] for key in existing.keys()}
                copy['id'] = result_id
                if existing == new:
                    # No change
                    pass
                else:
                    existing = set(existing.items())
                    new = set(new.items())
                    # print(
                    #     f"Updated result {r.id}: old: {existing - new}, new: {new - existing}")
                    results_to_update.append(copy)
            else:
                results_to_add.append(Result(**copy))

        for result in results_to_update:
            Result().find(result['id']).update(result)

        try:
            db.session.add_all(results_to_add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding horses: {e}")
            for res in results_to_add:
                try:
                    db.session.add(res)
                    db.session.commit()
                except:
                    db.session.rollback()
