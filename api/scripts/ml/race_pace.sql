WITH scoped_races AS (
  SELECT
    *
  FROM
    races
  WHERE
    date = {{date_input}}
),
pp365 AS (
  SELECT
    pp.id AS pp_id,
    res.race_id,
    res.horse_id,
    CASE WHEN pp.first_call_position <= 2 THEN
      1
    ELSE
      0
    END + CASE WHEN pp.first_call_lengths_back <= 2 THEN
      1
    ELSE
      0
    END AS pace,
    pp.beyer_or_foreign_speed,
    pp.first_call_lengths_back
  FROM
    results res
    INNER JOIN scoped_races ra ON res.race_id = ra.id
    INNER JOIN past_performances pp ON pp.horse_id = res.horse_id
  WHERE
    pp.race_date >= ra.date - interval '365 DAY'
    AND pp.race_date < ra.date
    AND pp.beyer_or_foreign_speed < 200
    AND pp.beyer_or_foreign_speed > 0
),
pp365_agg AS (
  SELECT
    pp365.race_id,
    pp365.horse_id,
    ROUND(AVG(pp365.pace), 4) AS pace,
    CASE WHEN AVG(pp365.first_call_lengths_back) <= 0 THEN
      'E'
    WHEN AVG(pp365.first_call_lengths_back) <= 2 THEN
      'E/P'
    WHEN AVG(pp365.first_call_lengths_back) IS NOT NULL THEN
      'P/S'
    END AS runstyle
  FROM
    pp365
  GROUP BY
    pp365.race_id,
    pp365.horse_id
)
SELECT
  pp.race_id,
  avg(pp.pace) AS race_pace,
  sum(
    CASE WHEN pp.runstyle = 'E' THEN
      1
    ELSE
      0
    END) AS count_early,
  sum(
    CASE WHEN pp.runstyle = 'E/P' THEN
      1
    ELSE
      0
    END) AS count_pacers,
  sum(
    CASE WHEN pp.runstyle = 'P/S' THEN
      1
    ELSE
      0
    END) AS count_closers,
  sum(
    CASE WHEN pp.runstyle IS NULL THEN
      1
    ELSE
      0
    END) AS count_unknown,
  count(*) AS field_size,
  sq.sprint,
  sq.turf
FROM
  results res
  INNER JOIN pp365_agg pp ON res.race_id = pp.race_id
    AND res.horse_id = pp.horse_id
  INNER JOIN (
    SELECT
      res.race_id,
      CASE WHEN c.surface = 't' THEN
        1
      ELSE
        0
      END AS turf,
      CASE WHEN c.distance < 8 THEN
        1
      ELSE
        0
      END AS sprint
    FROM
      results res
      INNER JOIN races ra ON res.race_id = ra.id
      INNER JOIN courses c ON ra.course_id = c.id) sq ON pp.race_id = sq.race_id
WHERE
  res.post_position < 30
  AND (res.scratched IS NULL
    OR NOT res.scratched)
GROUP BY
  pp.race_id,
  sq.sprint,
  sq.turf
