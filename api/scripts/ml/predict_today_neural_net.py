# import code

# import datetime
# from datetime import datetime as dt
# import sys

# import pandas as pd

# from main import app
# from app.models import Result
# from app.db import db
# from app.service_objects.ml import NeuralNetPredictor

# # Set today
# tracks = None
# if len(sys.argv) == 2:
#     predict_date = dt.date(dt.strptime(sys.argv[1], '%Y-%m-%d'))
# elif len(sys.argv) == 3:
#     predict_date = dt.date(dt.strptime(sys.argv[1], '%Y-%m-%d'))
#     tracks = sys.argv[2].split(',')
# else:
#     predict_date = dt.date(datetime.datetime.today())

# # Select data from today
# statement = open(
#     './scripts/ml/predict_today_neural_net.sql').read().replace('{{date_input}}', f"'{str(predict_date)}'")

# df = pd.read_sql(statement, db.engine)
# if tracks:
#     df = df.loc[df['track_code'].isin(tracks)].reset_index()

# # Call predictor on today
# predictions = NeuralNetPredictor(data=df).call()

# # Write report of some kind
# df = df.join(predictions, on='race_id', how='inner', rsuffix='pred')
# for index, result in df.iterrows():
#     result_id = result['result_id']
#     result_adj_pp = result['adj_post_position']
#     predictions = result['pred_win_probability']
#     predicted_prob = predictions[result_adj_pp]
#     result = Result().find(result_id)
#     result.update({'predicted_win_probability': predicted_prob})
