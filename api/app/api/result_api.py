from .base_model_api import BaseModelApi, db, json, datetime, pytz

import sys

import pandas as pd

from app.models import Result

from app.service_objects.ml import TensorFlowPredictorWrapper
from app.service_objects.ml import TensorFlowPredictor
from app.service_objects import LiveOddsScraper


class ResultApi(BaseModelApi):
    def __init__(self):
        pass

    class InvalidFilterError(Exception):
        pass

    def field_lookup(self, field):
        lookup = {
            'track_id': 'ra.track_id'
        }
        return lookup.get(field) or field

    def dtype_lookup(self, field):
        lookup = {
            'race_id': 'int',
            'trainer_id': 'int',
            'track_id': 'int',
            'course_id': 'int',
            'jockey_id': 'int',
            'owner_id': 'int',
            'horse_id': 'int',
            'distance': 'int',
            'date': 'date'
        }
        return lookup.get(field) or 'str'

    def opreator_lookup(self, operator):
        lookup = {
            'eq': '=',
            'gt': '>',
            'lt': '<',
            'gte': '>=',
            'lte': '<=',
            'in': 'in',
            'between': 'between'
        }
        return lookup.get(operator)

    def normalize_arguments(self, field, operator, arguments):
        ret = None
        if operator in ['eq', 'gt', 'lt', 'gte', 'lte']:
            if self.dtype_lookup(field) == 'int':
                ret = arguments[0]
            elif self.dtype_lookup(field) == 'date':
                ret = f"CAST('{arguments[0]}' AS DATE)"
            elif self.dtype_lookup(field) == 'str':
                ret = f"'{arguments[0]}'"
        elif operator == 'in':
            if self.dtype_lookup(field) == 'int':
                arguments = [str(arg) for arg in arguments]
                ret = '(' + ', '.join(arguments) + ')'
            elif self.dtype_lookup(field) == 'date':
                ret = "('" + \
                    "', '".join(
                        [f"CAST('{arg}' AS DATE)" for arg in arguments]) + "')"
            elif self.dtype_lookup(field) == 'str':
                ret = "('" + "', '".join(arguments) + "')"
        elif operator == 'between':
            if self.dtype_lookup(field) == 'int':
                ret = f"{arguments[0]} AND {arguments[1]}"
            elif self.dtype_lookup(field) == 'date':
                ret = f"CAST('{arguments[0]}' AS DATE) AND CAST('{arguments[1]}' AS DATE)"
            elif self.dtype_lookup(field) == 'str':
                ret = f"'{arguments[0]}' AND '{arguments[1]}'"
        return ret

    # example query = b'{"raceId":{"field":"race_id","operator":"eq","arguments":["1"]}}'

    def query(self, filter, entrants=False):
        filter = json.loads(filter)
        statement = '''
            SELECT res.id, h.name AS horse_name, res.horse_id, t.full_name AS trainer, res.trainer_id,
                j.full_name AS jockey, res.jockey_id, o.full_name AS owner, res.owner_id,
                res.race_id, ra.date AS race_date, courses.track_code, courses.distance, courses.surface, ra.race_number,
                res.race_id, res.post_position, res.program_number, res.final_position, res.odds,
                res.first_call_position, res.second_call_position, res.third_call_position,
                res.fourth_call_position, res.fifth_call_position, res.first_call_lengths_behind,
                res.second_call_lengths_behind, res.third_call_lengths_behind, res.fourth_call_lengths_behind,
                res.fifth_call_lengths_behind, res.morning_line_odds, res.scratched, res.predicted_win_probability, 
                res.predicted_individual_perf, extract(year from ra.date) - h.year_born age, h.sex, h.sire
            FROM results res INNER JOIN horses h ON res.horse_id = h.id
                INNER JOIN races ra ON res.race_id = ra.id
                INNER JOIN courses ON ra.course_id = courses.id
                INNER JOIN trainers t ON res.trainer_id = t.id
                INNER JOIN jockeys j ON res.jockey_id = j.id
                INNER JOIN owners o ON res.owner_id = o.id
        '''
        if entrants:
            clauses = []
        else:
            clauses = [
                'res.final_position > 0'
            ]
        for filter_element in filter:
            field = self.field_lookup(filter_element['field'])
            operator = self.opreator_lookup(filter_element['operator'])
            argument = self.normalize_arguments(
                filter_element['field'], filter_element['operator'], filter_element['arguments'])
            if field is None or operator is None or argument is None:
                raise InvalidFilterError
            clauses.append(f"{field} {operator} {argument}")

        if len(clauses) > 0:
            statement += "\nWHERE " + ' AND '.join(clauses)

        statement += "\nORDER BY ra.date DESC, courses.track_code ASC, ra.race_number ASC, res.post_position ASC LIMIT 1000"

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return json.dumps(ret)

    def list_entries(self, tracks):
        tz = pytz.timezone('EST')
        today = str(datetime.datetime.now(tz).date())
        tracks = json.loads(tracks)['data']
        statement = f'''
            SELECT res.id, t.code, ra.race_number, res.program_number, h.name
            FROM results res
                INNER JOIN races ra ON res.race_id = ra.id
                INNER JOIN tracks t ON ra.track_id = t.id
                INNER JOIN horses h ON res.horse_id = h.id
            WHERE ra.date = '{today}' AND t.id IN ({','.join(map(str, tracks))}) AND (res.scratched IS NULL OR NOT res.scratched)
            ORDER BY t.code ASC, ra.race_number ASC, res.program_number ASC
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return json.dumps(ret)

    def scratch_entry(self, id):
        entry = Result().find(id)
        entry.update({'scratched': True})
        return ''

    def predict(self):
        predict_date = datetime.datetime.today()

        # Select data from today
        statement = open(
            './scripts/ml/tensor_flow_input.sql').read().replace('{{date_input}}', f"'{str(predict_date)}'")

        df = pd.read_sql(statement, db.engine)

        # Call predictor on today
        predictions = TensorFlowPredictor(data=df).call()

        # Write report of some kind
        df = df.merge(predictions, on='race_id', how='inner')
        for index, result in df.iterrows():
            result_id = result['result_id']
            result_pp = result['post_position']
            predictions = result['pred_win_probability']
            predicted_prob = predictions[result_pp]
            result = Result().find(result_id)
            result.update({'predicted_win_probability': predicted_prob})

    def get_live_predictions(self, data):
        data = json.loads(data)['data']
        race_id = data['raceId']
        live_odds = data['liveOdds']
        wrapper = TensorFlowPredictorWrapper(
            race_id=race_id, live_odds=live_odds)
        df = wrapper.call()
        ret = []
        for i, result in df.iterrows():
            ret.append({
                'result_id': result.result_id,
                'program_number': result.program_number,
                'horse_name': result.horse_name,
                'implied_proba': result.implied_proba,
                'live_pred_win_probability': result.live_pred_win_probability
            })

        return json.dumps(ret)
