from .base_loader import BaseLoader

from app.models import PastPerformance
from app.db import db


class PastPerformanceLoader(BaseLoader):
    def insert_file_models(self, line_data):
        past_performance_key = self.model_cache.keygen([
            line_data['today_track'],
            line_data['today_date'],
            line_data['today_race_number'],
            line_data['horse_name'],
            line_data['race_date'],
        ])
        horse = self.model_cache.lookup('horse_sql', line_data['horse_name'])
        if not horse:
            # likely Qhorse race
            return

        self.model_cache.insert(
            'past_performance_file',
            past_performance_key,
            {
                'horse_id': self.model_cache.lookup('horse_sql', line_data['horse_name']).id,
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
                'owner': line_data['owner'],
                'comment': line_data['comment']
            }
        )

    def create_sql_records(self):
        past_performances_to_update = []
        past_performances_to_add = {}
        if 'past_performance_file' in self.model_cache.cache.keys():
            past_performances = self.model_cache.cache['past_performance_file']
        else:
            # No valid races in this file
            return

        for pp_key, past_performance in past_performances.items():
            pp = self.model_cache.lookup('past_performance_sql', pp_key)
            if not pp:
                pp = PastPerformance().find_by(**{
                    'horse_id': past_performance['horse_id'],
                    'track_code': past_performance['track_code'],
                    'race_date': past_performance['race_date']
                })
                if pp:
                    self.model_cache.insert('past_performance_sql', pp_key, pp)

            if pp:
                existing = pp.as_dict()
                new = PastPerformance(**past_performance).as_dict()
                new['id'] = existing['id']
                past_performance['id'] = pp.id
                if existing == new:
                    # No change
                    pass
                else:
                    # Happens too often
                    # existing = set(existing.items())
                    # new = set(new.items())
                    # print(
                    #     f"Updated past performance {pp.id}: old: {existing - new}, new: {new - existing}")
                    past_performances_to_update.append(past_performance)
            else:
                past_performances_to_add[pp_key] = PastPerformance(
                    **past_performance)

        for past_performance in past_performances_to_update:
            PastPerformance().find(
                past_performance['id']).update(past_performance)

        try:
            db.session.add_all(past_performances_to_add.values())
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
