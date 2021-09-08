from .base_model_api import BaseModelApi, db, json

from app.models import PastPerformance


class PastPerformanceAPI(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        return json.dumps(db.session.query(PastPerformance).filter(PastPerformance.id == id).first().as_dict())
