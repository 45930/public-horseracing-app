import json
from decimal import Decimal
import datetime
import re
import pytz

from app.db import db


class BaseModelApi():
    def __init__(self):
        pass

    def serialize(self, result):
        result = dict(result)
        ret = {}
        for key, value in result.items():
            if isinstance(value, Decimal):
                ret[key] = float(value)
            elif isinstance(value, datetime.date):
                ret[key] = str(value)
            else:
                ret[key] = value
        return ret
