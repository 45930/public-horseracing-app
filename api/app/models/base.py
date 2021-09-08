import datetime
from decimal import Decimal
from app.db import db


class Base(db.Model):

    __abstract__ = True

    def as_dict(self):
        ret = {}
        for c in self.__table__.columns:
            val = getattr(self, c.name)
            if isinstance(val, Decimal):
                ret[c.name] = float(val)
            elif isinstance(val, datetime.date):
                ret[c.name] = str(val)
            elif val is None:
                continue
            else:
                ret[c.name] = val
        return ret

    def create(self, **params):
        new_record = self.__class__(**params)
        session = db.session()
        try:
            session.add(new_record)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def find(self, id):
        session = db.session()
        ret = session.query(self.__class__).filter(
            self.__class__.id == id).first()
        session.close()
        return ret

    def find_by(self, **params):
        session = db.session()
        ret = session.query(self.__class__).filter_by(**params).first()
        session.close()
        return ret

    def find_or_create_by(self, **params):
        existing = self.find_by(**params)
        if not existing:
            self.create(**params)
            existing = self.find_by(**params)

        return existing

    def where(self, **params):
        session = db.session()
        ret = session.query(self.__class__).filter_by(**params)
        session.close()
        return ret

    def update(self, payload):
        db.session.query(self.__class__).filter(
            self.__class__.id == self.id).update(payload)
        db.session.commit()
        db.session.close()
