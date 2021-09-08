from .base_loader import BaseLoader

from app.models import Track, Course, Race
from app.db import db

BANNED_TRACK_CODES = ['bc', 'bfs', 'spl']


class RaceLoader(BaseLoader):
    def insert_file_models(self, line_data):
        if line_data['breed'] != "":
            if line_data['breed'] not in ['q', 'm', 'r']:
                print("Unknown breed found:")
                print(line_data['breed'])
            return

        track_code = line_data['track_code']
        if track_code in BANNED_TRACK_CODES:
            print(f"{track_code} is banned.... skipping")
            return

        course_key = self.model_cache.keygen([
            track_code,
            line_data['distance'],
            line_data['surface_code']
        ])
        race_key = self.model_cache.keygen([
            track_code,
            line_data['date'],
            line_data['race_number']
        ])
        self.model_cache.insert(
            'track_file',
            track_code,
            {
                'code': track_code,
                'name': line_data['track_name'],
                'state': line_data['state']
            }
        )
        self.model_cache.insert(
            'course_file',
            course_key,
            {
                'track_code': track_code,
                'distance': line_data['distance'],
                'surface': line_data['surface_code']
            }
        )
        self.model_cache.insert(
            'race_file',
            race_key,
            {
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
                'state': line_data['state'],
                'day_of_week': line_data['day_of_week'],
                'post_time': line_data['post_time'],
                'course_key': course_key
            }
        )

    def create_sql_records(self):
        if 'track_file' in self.model_cache.cache.keys():
            tracks = self.model_cache.cache['track_file']
        else:
            # No valid races in this file
            return

        for track_code, track in tracks.items():
            t = self.model_cache.lookup('track_sql', track_code)
            if not t:
                t = Track().find_or_create_by(**{'code': track['code']})
                t.update({
                    'name': track['name'],
                    'state': track['state']
                })
                t = Track().find(t.id)
                self.model_cache.insert('track_sql', track_code, t)

        courses = self.model_cache.cache['course_file']
        for course_key, course in courses.items():
            c = self.model_cache.lookup('course_sql', course_key)
            if not c:
                course['track_id'] = self.model_cache.lookup(
                    'track_sql', course['track_code']
                ).id
                c = Course().find_or_create_by(**course)
                self.model_cache.insert('course_sql', course_key, c)

        races = self.model_cache.cache['race_file']
        for race_key, race in races.items():
            r = self.model_cache.lookup('race_sql', race_key)
            if not r:
                race['track_id'] = self.model_cache.lookup(
                    'track_sql', race['track_code']
                ).id
                race['course_id'] = self.model_cache.lookup(
                    'course_sql', race['course_key']
                ).id
                r = Race().find_or_create_by(**({key: race[key] for key in [
                    'track_id',
                    'date',
                    'race_number'
                ]}))
                r.update({k: race[k]
                          for k in race.keys() - {'track_code', 'course_key'}})
                self.model_cache.insert('race_sql', race_key, r)
