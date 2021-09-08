import code
import re
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import time
import os

from app.service_objects.dataload import RaceDayLoader


# loader = RaceDayLoader(
#     'Cd_200516',
#     './sample_data/more/Cd_200516.cr',
#     './sample_data/more/Cd_200516.ch',
#     './sample_data/more/Cd_200516.chr'
# )


start_time = time.time()
directory = "./sample_data/using/"
files = [f for f in glob(f"{directory}*.*")]
track_dates = set()
for f in files:
    fname = os.path.basename(f)
    track = fname[0:3]
    date = fname[3:9]
    track_dates.add(''.join([track, date]))
for td in track_dates:
    loader = RaceDayLoader(
        td,
        f"{directory}{td}.cr",
        f"{directory}{td}.ch",
        f"{directory}{td}.pgh",
        f"{directory}{td}.chr"
    )
    loader.load_files()


print(f"Total run complete in {round(time.time() - start_time, 2)} seconds")
