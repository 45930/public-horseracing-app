from .base_model_api import BaseModelApi, db, json

from app.models import Horse


class HorseAPI(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        return json.dumps(db.session.query(Horse).filter(Horse.id == id).first().as_dict())

    def search(self, term):
        statement = f'''
            SELECT id, name, year_born, month_born
            FROM horses
            WHERE name LIKE '{term}%%'
            ORDER BY name DESC
            limit 50
        '''
        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return json.dumps(ret)

    def pastPerformances(self, id):
        statement = f'''
            SELECT pp.*
            FROM horses h INNER JOIN past_performances pp ON pp.horse_id = h.id
            WHERE h.id = {id}
            ORDER BY pp.race_date DESC
        '''
        with db.engine.connect() as conn:
            results = conn.execute(statement)

        ret = []
        for result in results:
            row = self.serialize(result)
            ret.append(row)

        return json.dumps(ret)
