from datetime import datetime, timedelta, timezone
import time
import pytz
from .base_model_api import BaseModelApi, db, json
import os

from app.models import Race

from app.service_objects import LiveOddsScraper


class RaceAPI(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        with db.engine.connect() as conn:
            races = conn.execute(
                f'''
                SELECT r.*, c.track_code, c.distance, c.surface
                FROM races r INNER JOIN courses c ON r.course_id = c.id
                WHERE r.id = {id}
                '''
            )

        ret = []
        for race in races:
            row = self.serialize(race)
            ret.append(row)

        return json.dumps(ret[0])

    def index(self):
        ret = []
        for result in db.session.query(Race).order_by(db.desc('date'), 'track_code', 'race_number').limit(100):
            ret.append(result.as_dict())
        return json.dumps(ret)

    def filter(self, params):
        return json.dumps({})

    def field_lookup(self, field):
        lookup = {
            'track_id': 'ra.track_id'
        }
        return lookup.get(field) or field

    def dtype_lookup(self, field):
        lookup = {
            'track_id': 'int',
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

    def query_cards(self, filter):
        filter = json.loads(filter)
        statement = '''
            SELECT ra.*, t.code AS track_code, c.distance, c.surface
            FROM races ra
            INNER JOIN tracks t ON ra.track_id = t.id
            INNER JOIN courses c on ra.course_id = c.id
            INNER JOIN (
                SELECT DISTINCT ra.id
                FROM races ra
                INNER JOIN results res ON res.race_id = ra.id
                WHERE res.final_position IS NOT NULL
            ) q on ra.id = q.id
        '''
        clauses = []
        for filter_element in filter:
            field = self.field_lookup(filter_element['field'])
            operator = self.opreator_lookup(filter_element['operator'])
            argument = self.normalize_arguments(
                filter_element['field'], filter_element['operator'], filter_element['arguments'])
            if field is None or operator is None or argument is None:
                raise InvalidFilterError
            clauses.append(f"{field} {operator} {argument}")

        if len(clauses) > 0:
            statement += " WHERE " + ' AND '.join(clauses)

        statement += "\nORDER BY ra.date DESC, t.code ASC LIMIT 1000"

        with db.engine.connect() as conn:
            races = conn.execute(statement)

        return self.assemble_cards(races)

    def recent_cards(self):
        with db.engine.connect() as conn:
            cards = conn.execute(
                '''
                SELECT t.code, r.date
                FROM races r
                INNER JOIN tracks t ON r.track_id = t.id
                INNER JOIN (
                    SELECT DISTINCT ra.id
                    FROM races ra
                    INNER JOIN results res ON res.race_id = ra.id
                    WHERE res.final_position IS NOT NULL
                ) q on r.id = q.id
                GROUP BY date, code
                ORDER BY date DESC
                LIMIT 10
                '''
            )

            min_date = min([card[1] for card in cards])

            races = conn.execute(
                db.text(
                    '''
                    SELECT r.id, c.track_code, r.date, r.race_number, r.classification, r.purse, c.distance, c.surface
                    FROM races r
                    INNER JOIN courses c on r.course_id = c.id
                    INNER JOIN (
                        SELECT DISTINCT ra.id
                        FROM races ra
                        INNER JOIN results res ON res.race_id = ra.id
                        WHERE res.final_position IS NOT NULL
                    ) q on r.id = q.id
                    WHERE r.date >= :min_date
                    '''),
                min_date=min_date
            )

        return self.assemble_cards(races)

    def today_races(self):
        tz = pytz.timezone('EST')
        today = str(datetime.now(tz).date())
        with db.engine.connect() as conn:
            races = conn.execute(
                db.text(
                    '''
                    SELECT r.id, c.track_code, r.date, r.race_number, r.classification, r.purse, c.distance, c.surface
                    FROM races r
                    INNER JOIN courses c on r.course_id = c.id
                    WHERE r.date >= :today
                    '''),
                today=today
                # today='2020-06-06'
            )
        return self.assemble_cards(races)

    def assemble_cards(self, races):
        cards = {}
        for race in races:
            key = f"{race['track_code']}|{str(race['date'])}"
            if cards.get(key):
                cards[key]['races'].append({
                    'id': race['id'],
                    'race_number': race['race_number'],
                    'track_code': race['track_code'],
                    'date': str(race['date']),
                    'classification': race['classification'],
                    'purse': int(race['purse'] * 1000),
                    'distance': float(race['distance']),
                    'surface': race['surface']
                })
            else:
                cards[key] = {
                    'races': [{
                        'id': race['id'],
                        'race_number': race['race_number'],
                        'track_code': race['track_code'],
                        'date': str(race['date']),
                        'classification': race['classification'],
                        'purse': int(race['purse'] * 1000),
                        'distance': float(race['distance']),
                        'surface': race['surface']
                    }]
                }

        ret = []
        for key, card in cards.items():
            card_key = key.split('|')
            card['races'].sort(key=(lambda race: race['race_number']))
            obj = {
                'track_code': card_key[0].upper(),
                'date': card_key[1],
                'races': card['races']
            }
            ret.append(obj)

        ret.sort(key=(lambda card: card['track_code']))
        ret.sort(reverse=True, key=(lambda card: card['date']))

        return json.dumps(ret)

    def past_performances(self, id):
        statement = f'''
            SELECT res.id result_id, pp.*
            FROM races ra INNER JOIN results res ON res.race_id = ra.id INNER JOIN horses h on res.horse_id = h.id INNER JOIN past_performances pp ON pp.horse_id = h.id
            WHERE ra.id = {id}
            ORDER BY pp.race_date DESC
        '''
        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = {}
        for result in results:
            result_id = result['result_id']
            if result_id in ret:
                if len(ret[result_id]) < 3:
                    ret[result_id].append(self.serialize(result))
            else:
                ret[result_id] = [self.serialize(result)]

        return json.dumps(ret)

    def live_odds(self, id):
        return json.dumps(LiveOddsScraper(id).scrape())

    def order_by_time(self):
        state_tz_lookup = {
            'ca': timezone(timedelta(hours=-8)),
            'il': timezone(timedelta(hours=-6)),
            'ar': timezone(timedelta(hours=-6))
        }
        tz = pytz.timezone('EST')
        today = str(datetime.now(tz).date())
        tracks = os.environ.get('PREFERRED_TRACKS').split(',')
        with db.engine.connect() as conn:
            races = conn.execute(
                f'''
                    SELECT r.id, c.track_code, r.date, r.race_number, r.classification, r.purse, c.distance, c.surface, r.post_time, r.state
                    FROM races r
                    INNER JOIN courses c on r.course_id = c.id
                    WHERE r.date = '{today}' AND c.track_code in ('{"','".join(map(str, tracks))}')
                '''
            )

        ret = []
        for race in races:
            race = self.serialize(race)
            if race['post_time']:
                post_time = f"2020-01-01 {race['post_time']}"
                tz = state_tz_lookup.get(race['state'])
                post_time = datetime.strptime(
                    post_time, "%Y-%m-%d %I:%M")
                if post_time.hour >= 9:
                    pass
                else:
                    post_time = post_time + timedelta(hours=12)
                if tz:
                    post_time = post_time.replace(tzinfo=tz)
                else:
                    post_time = post_time.replace(tzinfo=pytz.timezone('EST'))
                race['post_time'] = post_time
                ret.append(race)

        actual_ret = []
        ret.sort(key=(lambda x: x['post_time']))
        for thing in ret:
            thing['post_time'] = (thing['post_time']).astimezone(
                pytz.timezone('EST')).strftime('%I:%M %p')

        return json.dumps(ret)
