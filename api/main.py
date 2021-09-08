from flask import Flask, request
from flask_cors import CORS
from flask_caching import Cache
import os
import json
import tensorflow as tf
import threading

app = Flask(__name__)

config = {
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}


app.config.from_mapping(config)
app.config.update(os.environ)
cors = CORS(app, resources={
            r"/api/*": {"origins": f"{app.config['ALLOWED_ORIGINS']}"}})
cache = Cache(app)

live_odds_model = tf.keras.models.load_model(
    './app/service_objects/ml/tensor_flow/model_odds_2021_02_07_2.keras_model')

from app.models import *  # noqa: E402
from app.api import *  # noqa: E402


horse_api = HorseAPI()
race_api = RaceAPI()
result_api = ResultApi()
trainer_api = TrainerAPI()
jockey_api = JockeyApi()
owner_api = OwnerApi()
track_api = TrackAPI()


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    data = str(hash(frozenset(request.data)))
    return (path + args + data).encode('utf-8')


@app.route('/api/horses/<id>')
@cache.cached(timeout=100)
def show_horse(id):
    return horse_api.show(id)


@app.route('/api/horses/search', methods=["POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def search_horse():
    term = json.loads(request.data)['term']
    return horse_api.search(term)


@app.route('/api/horses/<id>/past_performances')
@cache.cached(timeout=100)
def horse_past_performances(id):
    return horse_api.pastPerformances(id)


@app.route('/api/races/', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def races():
    if request.method == "POST":
        return race_api.query_cards(request.data)
    else:
        return race_api.index()


@app.route('/api/races/<id>')
@cache.cached(timeout=100)
def show_race(id):
    return race_api.show(id)


@app.route('/api/races/<id>/past_performances')
@cache.cached(timeout=100)
def fetch_race_past_performances(id):
    return race_api.past_performances(id)


@app.route('/api/races/<id>/live_odds')
@cache.cached(timeout=10)
def fetch_race_live_odds(id):
    return race_api.live_odds(id)


@app.route('/api/races/order_by_time')
@cache.cached(timeout=100)
def order_by_time():
    return race_api.order_by_time()


@app.route('/api/cards/')
@cache.cached(timeout=100)
def recent_cards():
    return race_api.recent_cards()


@app.route('/api/entrants/', methods=["GET", "POST"])
def entrants():
    if request.method == "POST":
        return result_api.query(request.data, entrants=True)
    return race_api.today_races()


@app.route('/api/trainers/top', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def top_trainers():
    if request.method == "POST":
        return trainer_api.top(request.data)
    return trainer_api.top()


@app.route('/api/trainers/<id>')
@cache.cached(timeout=100)
def show_trainer(id):
    return trainer_api.show(id)


@app.route('/api/trainers/')
@cache.cached(timeout=100)
def index_trainers():
    return trainer_api.index()


@app.route('/api/trainers/stats/<id>', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def trainer_stats(id):
    if request.method == "POST":
        return trainer_api.stats(id, request.data)
    return trainer_api.stats(id)


@app.route('/api/jockeys/top', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def top_jockeys():
    if request.method == "POST":
        return jockey_api.top(request.data)
    return jockey_api.top()


@app.route('/api/jockeys/<id>')
@cache.cached(timeout=100)
def show_jockey(id):
    return jockey_api.show(id)


@app.route('/api/jockeys/')
@cache.cached(timeout=100)
def index_jockeys():
    return jockey_api.index()


@app.route('/api/jockeys/stats/<id>', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def jockey_stats(id):
    if request.method == "POST":
        return jockey_api.stats(id, request.data)
    return jockey_api.stats(id)


@app.route('/api/owners/<id>')
@cache.cached(timeout=100)
def show_owner(id):
    return owner_api.show(id)


@app.route('/api/owners/stats/<id>', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def owner_stats(id):
    if request.method == "POST":
        return owner_api.stats(id, request.data)
    return owner_api.stats(id)


@app.route('/api/results/', methods=["GET", "POST"])
@cache.cached(timeout=100, key_prefix=make_cache_key)
def results():
    if request.method == "POST":
        return result_api.query(request.data)


@app.route('/api/list_entries', methods=['POST'])
def list_entries():
    return result_api.list_entries(request.data)


@app.route('/api/scratch_entry/<id>')
def scratch_entry(id):
    return result_api.scratch_entry(id)


@app.route('/api/tracks/<id>')
@cache.cached(timeout=100)
def show_track(id):
    return track_api.show(id)


@app.route('/api/tracks/')
@cache.cached(timeout=1000)
def index_tracks():
    return track_api.index()


@app.route('/api/get_live_prediction', methods=['POST'])
@cache.cached(timeout=10)
def get_live_prediction():
    return result_api.get_live_predictions(request.data)


@app.route('/api/predict', methods=['GET'])
def predict():
    thread = threading.Thread(target=result_api.predict)
    thread.start()
    return {"message": "Accepted"}, 202


if __name__ == "__main__":
    app.run()
