WITH scoped_races AS (
  SELECT
    *
  FROM
    races
  WHERE
    id = {{race_id}}
),
scoped_results AS (
  SELECT
    res.*
  FROM
    results res
    INNER JOIN scoped_races ON res.race_id = scoped_races.id
  WHERE (res.scratched IS NULL
    OR NOT res.scratched)
),
race_averages AS (
  SELECT
    race_id,
    COUNT(*) AS field_size
FROM
  scoped_results
GROUP BY
  race_id
),
prediction_data AS (
  SELECT
    res.race_id,
    res.horse_id,
    res.id AS result_id,
    res.program_number,
    res.post_position,
    h.name AS horse_name,
    r_avg.field_size,
    predicted_win_probability
  FROM
    scoped_results res
    INNER JOIN horses h ON res.horse_id = h.id
    INNER JOIN race_averages r_avg ON res.race_id = r_avg.race_id
)
SELECT
  pd.result_id,
  pd.race_id,
  pd.horse_id,
  pd.program_number,
  pd.horse_name,
  pd.predicted_win_probability,
  rank() OVER (PARTITION BY pd.race_id ORDER BY pd.post_position ASC) AS adj_post_position
  FROM
    prediction_data pd
