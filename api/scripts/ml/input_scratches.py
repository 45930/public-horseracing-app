from main import app
from app.models import Race, Track, Course
from app.db import db

import csv


scratches = csv.DictReader(open('./scripts/ml/scratches.csv'),
                           delimiter=',', quotechar='"', strict=True)

for scratch in scratches:
    statement = f"""
      UPDATE results res
      SET scratched = TRUE
      FROM races ra INNER JOIN courses c ON ra.course_id = c.id
      WHERE ra.date = '{scratch['date']}'  AND res.race_id = ra.id
      AND ra.race_number = {scratch['race_number']} 
      AND c.track_code = '{scratch['track_code']}'
      AND res.program_number = '{scratch['program_number']}'
    """

    with db.engine.connect() as conn:
        conn.execute(statement)
