from .base_loader import BaseLoader, date, re, csv

from app.models import Track, Race, Horse, Result
from app.db import db


class ResultLoader(BaseLoader):
    # Overriding base loader
    def load(self):
        with open(self.file) as open_file:
            lines = self.parse_csv(open_file)
            headers = next(lines)
            if headers[0] != 'H':
                return

            self.track_code = headers[2].replace(' ', '').lower()
            race_date = headers[3]
            y = int(race_date[0:4])
            m = int(race_date[4:6])
            d = int(race_date[6:8])
            self.race_date = date(y, m, d)
            try:
                for line in lines:
                    if line[0] == 'S':
                        line_data = self.get_line_data(line, self.schema)
                        self.insert_file_models(line_data)
            except csv.Error:
                print(f"$ ERROR: Could not strictly parse csv: {self.file}")
                return

            if 'result_file' not in self.model_cache.cache.keys():
                print(f"$ Error: Result {self.file} contains no results")
                return

            self.create_sql_records()

    def insert_file_models(self, line_data):
        result_key = self.model_cache.keygen([
            self.track_code,
            line_data['race_number'],
            self.race_date,
            line_data['horse_name']
        ])
        foal_date = line_data['foal_date']
        year_born = int(foal_date[0:4])
        month_born = int(foal_date[5:6])
        self.model_cache.insert(
            'result_file',
            result_key,
            {
                # Foriegn horses come like "horse name (country code)" -- This removes the country code
                'horse_name': re.sub('\s\(([^)]+)\)', '', line_data['horse_name']),
                'race_number': line_data['race_number'],
                'year_born': year_born,
                'month_born': month_born,
                'odds': line_data['odds'],
                'post_position': line_data['post_position'],
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
            }
        )

    def create_sql_records(self):
        results = self.model_cache.cache['result_file']
        track = Track().find_by(**{'code': self.track_code})
        if not track:
            print(f"Track not found: {self.track_code}")
            return
        for result_key, result in results.items():
            race = Race().find_by(**{
                'track_id': track.id,
                'date': self.race_date,
                'race_number': result['race_number']
            })
            horse = Horse().find_by(**{
                'name': result['horse_name'],
                'year_born': result['year_born'],
                'month_born': result['month_born']
            })
            if not race or not horse:
                # too noisy when not debugging
                # print(
                #     f"race or horse not found... race: {race} horse: {horse} (track: {self.track_code}, date: {self.race_date}, race_number: {result['race_number']}, horse_name: {result['horse_name']}, program number: {result['program_number']})")
                continue

            copy = {
                k: result[k]
                for k in result.keys() - {
                    'race_number',
                    'horse_name',
                    'year_born',
                    'month_born',
                }
            }
            r = Result().find_by(**{
                'race_id': race.id,
                'horse_id': horse.id
            })
            if not r:
                print(f"result not found race: {race}, horse: {horse}")
                print(
                    f"Result for not found: Finish pos: {result['final_position']}")
                continue
            r.update(copy)
