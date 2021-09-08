import code
import re
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
import os

from app.service_objects.dataload import ResultLoaderWrapper

start_time = time.time()
directory = "./sample_data/using/results/"
files = [f for f in glob(f"{directory}*.chart")]
track_dates = set()
track_name_regex = r"^[A-z]+"
race_date_regex = r"[0-9]+"
for f in files:
    fname = os.path.basename(f)
    track = re.search(track_name_regex, fname)
    date = re.search(race_date_regex, fname)
    track_dates.add(''.join([track.group(), date.group()]))
for td in track_dates:
    loader = ResultLoaderWrapper(
        td,
        f"{directory}{td}.chart"
    )
    loader.load_files()


print(f"Total run complete in {round(time.time() - start_time, 2)} seconds")
