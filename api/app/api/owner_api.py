import os
from .base_model_api import BaseModelApi, db, json, datetime

from app.models import Owner

time_range = int(os.environ.get('DFAULT_TIME_RANGE'))


class OwnerApi(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        return json.dumps(db.session.query(Owner).filter(Owner.id == id).first().as_dict())

    def stats(self, id, after=None):
        after = json.loads(after)['after']
        if after is None:
            after = time_range

        date_input = datetime.datetime.today() - datetime.timedelta(days=after)
        ret = {
            'trainer_stats': self.trainer_stats(id, date_input),
            'jockey_stats': self.jockey_stats(id, date_input),
            'class_stats': self.class_stats(id, date_input),
            'surface_stats': self.surface_stats(id, date_input),
        }

        return json.dumps(ret)

    # private
    def jockey_stats(self, id, date_input):
        statement = f'''
            WITH applicable_results AS (
                SELECT owner_id, r.id as result_id, race_id, final_position, jockey_id, j.full_name AS jockey_name
                FROM results r 
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN jockeys j on r.jockey_id = j.id
                WHERE owner_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), jockey_wins AS (
                SELECT ar.jockey_id, count(ar.owner_id) AS wins
                FROM applicable_results ar
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.jockey_id
            )

            SELECT ar.jockey_name AS full_name, ar.jockey_id AS id, count(owner_id) AS starts, COALESCE(sq.wins, 0) AS wins
            FROM applicable_results ar
                LEFT JOIN jockey_wins sq ON ar.jockey_id = sq.jockey_id
            GROUP BY ar.jockey_name, ar.jockey_id, COALESCE(sq.wins, 0)
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
                SELECT owner_id, r.id as result_id, race_id, final_position, trainer_id, t.full_name AS trainer_name
                FROM results r
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN trainers t on r.trainer_id = t.id
                WHERE owner_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), trainer_wins AS (
                SELECT ar.trainer_id, count(ar.owner_id) AS wins
                FROM applicable_results ar
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.trainer_id
            )

            SELECT ar.trainer_name AS full_name, ar.trainer_id AS id, count(owner_id) AS starts, COALESCE(sq.wins, 0) AS wins
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
                SELECT owner_id, r.id as result_id, race_id, final_position, ra.classification
                FROM results r INNER JOIN races ra on r.race_id = ra.id
                WHERE owner_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), class_wins AS (
                SELECT ar.classification, count(ar.owner_id) AS wins
                FROM applicable_results ar
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.classification
            )

            SELECT ar.classification, count(owner_id) AS starts, COALESCE(sq.wins, 0) AS wins
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
                SELECT c.id, c.surface, CASE WHEN c.distance >= 8 THEN 1 ELSE 0 END AS route, owner_id, r.id as result_id, race_id, final_position
                FROM results r
                    INNER JOIN races ra on r.race_id = ra.id
                    INNER JOIN courses c on ra.course_id = c.id
                WHERE owner_id = {id} AND final_position > 0 AND ra.date > '{date_input}'
            ), surface_wins AS (
                SELECT ar.route, ar.surface, count(ar.owner_id) AS wins
                FROM applicable_results ar
                    INNER JOIN results res ON res.id = ar.result_id
                WHERE res.final_position = 1
                GROUP BY ar.route, ar.surface
            )

            SELECT ar.route, ar.surface, count(owner_id) AS starts, COALESCE(sq.wins, 0) AS wins
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
