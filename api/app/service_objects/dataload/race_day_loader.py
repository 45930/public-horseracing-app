import json
import time

from .file_loaders import RaceLoader, HorseLoader, PastPerformanceLoader
from .model_cache import ModelCache


class RaceDayLoader():
    def __init__(self, track_date, race_file, horse_file, betting_info_file, past_performance_file):
        self.model_cache = ModelCache()
        self.track_date = track_date
        self.race_file = race_file
        self.horse_file = horse_file
        self.betting_info_file = betting_info_file
        self.past_performance_file = past_performance_file

    def load_files(self):
        start_time = time.time()
        race_schema = json.load(open('./file_definitions.json'))['race_file']
        horse_schema = json.load(open('./file_definitions.json'))['horse_file']
        betting_info_schema = json.load(
            open('./file_definitions.json'))['betting_info_file']
        past_performance_schema = json.load(
            open('./file_definitions.json'))['past_performance_file']

        print(f"$ processing files for {self.track_date} $")
        RaceLoader(self.race_file, self.model_cache, race_schema).load()
        HorseLoader(self.horse_file, self.model_cache, horse_schema,
                    self.betting_info_file, betting_info_schema).load()
        PastPerformanceLoader(self.past_performance_file,
                              self.model_cache,
                              past_performance_schema).load()
        print(
            f"$ completed processing files for {self.track_date} in {round(time.time() - start_time, 1)} seconds $")
