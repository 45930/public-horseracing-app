import json
import time

from .model_cache import ModelCache
from .file_loaders import ResultLoader


class ResultLoaderWrapper():
    def __init__(self, track_date, result_file):
        self.model_cache = ModelCache()
        self.track_date = track_date
        self.result_file = result_file

    def load_files(self):
        start_time = time.time()
        result_schema = json.load(
            open('./file_definitions.json'))['results_file']

        print(f"$ processing result for {self.track_date} $")
        ResultLoader(self.result_file, self.model_cache, result_schema).load()
        print(
            f"$ completed processing files for {self.track_date} in {round(time.time() - start_time, 1)} seconds $")
