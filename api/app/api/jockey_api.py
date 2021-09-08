import os

from .base_model_api import BaseModelApi, db, json, datetime

from app.models import Jockey

time_range = int(os.environ.get('DFAULT_TIME_RANGE'))


class JockeyApi(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        return json.dumps(db.session.query(Jockey).filter(Jockey.id == id).first().as_dict())

    def index(self):
        return json.dumps([row.as_dict() for row in db.session.query(Jockey).order_by('full_name').all()])

    def stats(self, id, after=None):
        after = json.loads(after)['after']
        if after is None:
            after = time_range

        date_input = datetime.datetime.today() - datetime.timedelta(days=after)
        ret = {
            'track_stats': self.track_stats(id, date_input),
            'trainer_stats': self.trainer_stats(id, date_input),
            'class_stats': self.class_stats(id, date_input),
            'surface_stats': self.surface_stats(id, date_input),
        }

        return json.dumps(ret)

    def top(self, after=None):
        after = json.loads(after)['after']
        if after is None:
            after = time_range
        date_input = datetime.datetime.today() - datetime.timedelta(days=after)
        statement = f'''
            WITH applicable_results AS (
                SELECT trainer_id, t.full_name, r.id as result_id, race_id, r.final_position
                FROM results r 
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN trainers t on r.trainer_id = t.id
                WHERE r.final_position > 0 AND ra.date > '{date_input}'
            ), trainer_wins AS (
                SELECT ar.trainer_id, count(ar.trainer_id) AS wins
                FROM applicable_results ar 
                    INNER JOIN results res ON ar.result_id = res.id
                    INNER JOIN races r ON ar.race_id = r.id
                WHERE res.final_position = 1 AND r.date > '{date_input}'
                GROUP BY ar.trainer_id
            )

            SELECT ar.trainer_id, ar.full_name, count(ar.trainer_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                INNER JOIN races r ON ar.race_id = r.id
                LEFT JOIN trainer_wins sq ON ar.trainer_id = sq.trainer_id
            GROUP BY ar.trainer_id, ar.full_name, COALESCE(sq.wins, 0)
            ORDER BY COALESCE(sq.wins, 0) DESC
            LIMIT 20
        '''
        statement = f'''
        WITH applicable_results AS (
            SELECT jockey_id, j.full_name, r.id as result_id, race_id, r.final_position
            FROM results r 
                INNER JOIN races ra on r.race_id = ra.id
                INNER JOIN jockeys j on r.jockey_id = j.id
            WHERE r.final_position > 0 AND ra.date > '{date_input}'
        ), jockey_wins AS (
            SELECT ar.jockey_id, count(ar.jockey_id) AS wins
            FROM applicable_results ar 
                INNER JOIN results res ON ar.result_id = res.id
                INNER JOIN races r ON ar.race_id = r.id
            WHERE res.final_position = 1 AND r.date > '{date_input}'
            GROUP BY ar.jockey_id
        )

        SELECT ar.jockey_id AS id, ar.full_name, count(ar.jockey_id) AS starts, COALESCE(sq.wins, 0) AS wins
        FROM applicable_results ar
            INNER JOIN races r ON ar.race_id = r.id
            LEFT JOIN jockey_wins sq ON ar.jockey_id = sq.jockey_id
        GROUP BY ar.jockey_id, ar.full_name, COALESCE(sq.wins, 0)
        ORDER BY COALESCE(sq.wins, 0) DESC
        LIMIT 20
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return json.dumps(ret)

    # private
    def track_stats(self, id, date_input):
        statement = f'''
            WITH applicable_results AS (
                SELECT jockey_id, r.id as result_id, race_id, r.final_position
                FROM results r INNER JOIN races ra on r.race_id = ra.id
                WHERE jockey_id = {id} AND r.final_position > 0 AND ra.date > '{date_input}'
            ), track_wins AS (
                SELECT tracks.code, count(ar.jockey_id) AS wins
                FROM applicable_results ar INNER JOIN results res ON res.id = ar.result_id
                    INNER JOIN races ra ON res.race_id = ra.id
                    INNER JOIN tracks ON ra.track_id = tracks.id
                WHERE ar.jockey_id = {id} AND res.final_position = 1 AND ra.date > '{date_input}'
                GROUP BY tracks.code
            )
            
            SELECT tracks.code AS track_code, count(ar.jockey_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                INNER JOIN races ra ON ar.race_id = ra.id
                INNER JOIN tracks ON ra.track_id = tracks.id
                LEFT JOIN track_wins sq ON tracks.code = sq.code
            GROUP BY tracks.code, COALESCE(sq.wins, 0)
            ORDER BY COALESCE(wins, 0) DESC
            LIMIT 10
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return ret

    # private
    def trainer_stats(self, id, date_input):
        statement = f'''
            WITH applicable_results AS (
                SELECT jockey_id, r.id as result_id, race_id, final_position, trainer_id, t.full_name AS trainer_name
                FROM results r 
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN trainers t on r.trainer_id = t.id
                WHERE jockey_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), trainer_wins AS (
                SELECT ar.trainer_id, count(ar.jockey_id) AS wins
                FROM applicable_results ar 
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.trainer_id
            )

            SELECT ar.trainer_name AS full_name, ar.trainer_id AS id, count(jockey_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                LEFT JOIN trainer_wins sq ON ar.trainer_id = sq.trainer_id
            GROUP BY ar.trainer_name, ar.trainer_id, COALESCE(sq.wins, 0)
            ORDER BY COALESCE(wins, 0) DESC
            LIMIT 10
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return ret

    # private
    def class_stats(self, id, date_input):
        statement = f'''
            WITH applicable_results AS (
                SELECT jockey_id, r.id as result_id, race_id, final_position, ra.classification
                FROM results r INNER JOIN races ra on r.race_id = ra.id
                WHERE jockey_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), class_wins AS (
                SELECT ar.classification, count(ar.jockey_id) AS wins
                FROM applicable_results ar 
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.classification
            )

            SELECT ar.classification, count(jockey_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                LEFT JOIN class_wins sq ON ar.classification = sq.classification
            GROUP BY ar.classification, COALESCE(sq.wins, 0)
            ORDER BY COALESCE(wins, 0) DESC
            LIMIT 10
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return ret

    # private
    def surface_stats(self, id, date_input):
        statement = f'''
            WITH applicable_results AS (
                SELECT c.id, c.surface, CASE WHEN c.distance >= 8 THEN 1 ELSE 0 END AS route, jockey_id, r.id as result_id, race_id, final_position
                FROM results r 
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN courses c on ra.course_id = c.id
                WHERE jockey_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), surface_wins AS (
                SELECT ar.route, ar.surface, count(ar.jockey_id) AS wins
                FROM applicable_results ar 
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.route, ar.surface
            )

            SELECT ar.route, ar.surface, count(jockey_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                LEFT JOIN surface_wins sq ON ar.route = sq.route AND ar.surface = sq.surface
            GROUP BY ar.route, ar.surface, COALESCE(sq.wins, 0)
            ORDER BY COALESCE(wins, 0) DESC
            LIMIT 10
        '''

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return ret
