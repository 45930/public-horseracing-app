import code
import numpy as np
import pandas as pd
import pickle
import os

import sys

import datetime
from datetime import datetime as dt

from sqlalchemy import create_engine
import sklearn.model_selection as model_selection

from main import app
from app.models import Race
from app.db import db

from app.service_objects.ml import RacePacePredictor

# tracks = None
# if len(sys.argv) == 2:
#     predict_date = dt.date(dt.strptime(sys.argv[1], '%Y-%m-%d'))
# elif len(sys.argv) == 3:
#     predict_date = dt.date(dt.strptime(sys.argv[1], '%Y-%m-%d'))
#     tracks = sys.argv[2].split(',')
# else:
#     predict_date = dt.date(datetime.datetime.today())

# statement = open(
#     './scripts/ml/race_pace.sql').read().replace('{{date_input}}', f"'{str(predict_date)}'")


# df = pd.read_sql(statement, db.engine)
# df = df.fillna(0)

# df['pct_early'] = df.count_early / df.field_size
# df['pct_pacers'] = df.count_pacers / df.field_size
# df['pct_closers'] = df.count_closers / df.field_size
# df['pct_unknown'] = df.count_unknown / df.field_size

# df = RacePacePredictor(data=df).call()

# for i, race in df.iterrows():
#     pred_closer = round(race.predicted_paces['CLOSER'], 4)
#     pred_pace = round(race.predicted_paces['PACE'], 4)
#     pred_wire = round(race.predicted_paces['WIRE'], 4)
#     race_model = Race().find(race.race_id)
#     race_model.update({
#         'predicted_closer_percent': pred_closer,
#         'predicted_pacer_percent': pred_pace,
#         'predicted_wire_percent': pred_wire
#     })
