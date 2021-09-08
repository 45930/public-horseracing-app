import code

import datetime
from datetime import datetime as dt
import sys

import pandas as pd

from main import app
from app.models import Result
from app.db import db
from app.service_objects.ml import TensorFlowPredictor


class TensorFlowPredictorWrapper(object):
    def __init__(self, race_id, live_odds):
        self.race_id = race_id
        self.live_odds = live_odds

    def call(self):
        statement = open(
            './scripts/ml/tensor_input_api.sql').read().replace('{{race_id}}', str(self.race_id))
        df = pd.read_sql(statement, db.engine)
        odds_vector = []
        for index, result in df.iterrows():
            result_id = str(int(result['result_id']))
            if result_id in self.live_odds.keys():
                odds_vector.append(
                    118 / (100 + float(self.live_odds[result_id])))
            else:
                odds_vector.append(0)
        df['implied_proba'] = odds_vector
        predictions = TensorFlowPredictor(
            data=df, use_odds=True).call()
        df = df.merge(predictions, on='race_id', how='inner')
        prob_vector = []
        for index, result in df.iterrows():
            result_id = result['result_id']
            result_pp = result['post_position']
            predictions = result['pred_win_probability_live']
            predicted_prob = predictions[result_pp]
            prob_vector.append(predicted_prob)

        df['live_pred_win_probability'] = prob_vector
        df.implied_proba = (df.implied_proba / 1.18).round(3)
        return df[['result_id', 'program_number', 'horse_name', 'implied_proba', 'live_pred_win_probability']]
