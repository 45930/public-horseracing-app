from .base_model_api import BaseModelApi, db, json

from app.models import Track


class TrackAPI(BaseModelApi):
    def __init__(self):
        pass

    def show(self, id):
        return json.dumps(db.session.query(Track).filter(Track.id == id).first().as_dict())

    def index(self):
        return json.dumps([row.as_dict() for row in db.session.query(Track).order_by('code').all()])
