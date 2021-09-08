WITH scoped_races AS (
  SELECT
    *
  FROM
    races
  WHERE
    id = {{race_id}}
),
_historical_pps AS (
  SELECT
    result_id,
    pp_count,
    wpps.perf / wpps.weights_sum perf,
    wpps.beyer / wpps.weights_sum beyer,
    wpps.first_call_position / wpps.weights_sum first_call_position,
    wpps.second_call_position / wpps.weights_sum second_call_position
  FROM (
    SELECT
      result_id,
      SUM(perf * weights) perf,
      SUM(beyer * weights) beyer,
    SUM(first_call_position * weights) first_call_position,
    SUM(second_call_position * weights) second_call_position,
    SUM(weights) weights_sum,
    COUNT(result_id) pp_count
  FROM (
    SELECT
      pp.id AS pp_id,
      r.id AS race_id,
      res.id AS result_id,
      pp.race_date,
      r.date - pp.race_date days_since, -- preproc to days since
      pp.distance, -- scale between 5 - 12 f
      LN(CAST(pp.purse AS float) + 1) AS purse, -- ln
      pp.track_code, -- factor
      pp.surface, -- factor
      pp.race_class, -- factor
      c.surface race_surface,
      c.distance race_distance,
      CAST(pp.first_call_position - 1 AS float) / (pp.field_size - 1) first_call_position,
      pp.first_call_lengths_back,
      CAST(pp.second_call_position - 1 AS float) / (pp.field_size - 1) second_call_position,
      pp.second_call_lengths_back,
      CAST(pp.final_call_position - 1 AS float) / (pp.field_size - 1) final_call_position,
      pp.final_call_lengths_back,
      CASE WHEN pp.foreign_or_domestic != 'f' THEN
        CAST(pp.beyer_or_foreign_speed AS float) / 100
      END beyer,
      LN(pp.beyer_or_foreign_speed + 1) + LN(CAST(pp.purse AS float) / 8) - 1.2 * CASE WHEN pp.final_call_position = 1 THEN
        0
      ELSE
        LN(final_call_lengths_back)
      END perf,
      1.0 / (r.date - pp.race_date) weights
    FROM
      past_performances pp
      INNER JOIN horses h ON pp.horse_id = h.id
      INNER JOIN results res ON res.horse_id = h.id
      INNER JOIN scoped_races r ON res.race_id = r.id
      INNER JOIN tracks t ON r.track_id = t.id
      INNER JOIN courses c ON c.id = r.course_id
    WHERE
      1 = 1
      -- AND t.code IN ('sar', 'ap', 'sa', 'bel', 'gg', 'cd', 'op', 'gp', 'tam', 'aqu', 'kee', 'dmr', 'wo', 'pim', 'ded', 'del', 'elp')
      AND r.date > pp.race_date
      AND c.distance >= 5
      AND c.distance <= 12
      AND pp.beyer_or_foreign_speed > 0
      AND pp.beyer_or_foreign_speed < 200
      AND pp.foreign_or_domestic = 'd'
      AND pp.field_size > 1
      AND pp.final_call_position > 0
      AND pp.final_call_position < 20
      AND pp.purse > 0
      AND pp.final_call_lengths_back >= 0) pps
  GROUP BY
    result_id) wpps
),
_similar_pps AS (
  SELECT
    result_id,
    dslr,
    wpps.perf / wpps.weights_sum perf,
    wpps.beyer / wpps.weights_sum beyer,
    wpps.first_call_position / wpps.weights_sum first_call_position,
    wpps.second_call_position / wpps.weights_sum second_call_position
  FROM (
    SELECT
      result_id,
      SUM(perf * weights) perf,
    SUM(beyer * weights) beyer,
    SUM(first_call_position * weights) first_call_position,
    SUM(second_call_position * weights) second_call_position,
    SUM(weights) weights_sum,
    min(days_since) dslr
  FROM (
    SELECT
      pp.id AS pp_id,
      r.id AS race_id,
      res.id AS result_id,
      pp.race_date,
      r.date - pp.race_date days_since, -- preproc to days since
      pp.distance, -- scale between 5 - 12 f
      LN(CAST(pp.purse AS float) + 1) AS purse, -- ln
      pp.track_code, -- factor
      pp.surface, -- factor
      pp.race_class, -- factor
      c.surface race_surface,
      c.distance race_distance,
      CAST(pp.first_call_position - 1 AS float) / (pp.field_size - 1) first_call_position,
      pp.first_call_lengths_back,
      CAST(pp.second_call_position - 1 AS float) / (pp.field_size - 1) second_call_position,
      pp.second_call_lengths_back,
      CAST(pp.final_call_position - 1 AS float) / (pp.field_size - 1) final_call_position,
      pp.final_call_lengths_back,
      CASE WHEN pp.foreign_or_domestic != 'f' THEN
        CAST(pp.beyer_or_foreign_speed AS float) / 100
      END beyer,
      LN(pp.beyer_or_foreign_speed + 1) + LN(CAST(pp.purse AS float) / 8) - 1.2 * CASE WHEN pp.final_call_position = 1 THEN
        0
      ELSE
        LN(final_call_lengths_back)
      END perf,
      1.0 / (r.date - pp.race_date) weights
    FROM
      past_performances pp
      INNER JOIN horses h ON pp.horse_id = h.id
      INNER JOIN results res ON res.horse_id = h.id
      INNER JOIN scoped_races r ON res.race_id = r.id
      INNER JOIN tracks t ON r.track_id = t.id
      INNER JOIN courses c ON c.id = r.course_id
    WHERE
      1 = 1
      -- AND t.code IN ('sar', 'ap', 'sa', 'bel', 'gg', 'cd', 'op', 'gp', 'tam', 'aqu', 'kee', 'dmr', 'wo', 'pim', 'ded', 'del', 'elp')
      AND r.date > pp.race_date
      AND c.distance >= 5
      AND c.distance <= 12
      AND pp.beyer_or_foreign_speed > 0
      AND pp.beyer_or_foreign_speed < 200
      AND pp.foreign_or_domestic = 'd'
      AND pp.field_size > 1
      AND pp.final_call_position > 0
      AND pp.final_call_position < 20
      AND pp.purse > 0
      AND pp.final_call_lengths_back >= 0) pps
    INNER JOIN scoped_races r ON r.id = pps.race_id
    INNER JOIN courses c ON c.id = r.course_id
  WHERE
    c.surface = pps.surface
    AND c.distance <= pps.distance + 1.0
    AND c.distance >= pps.distance - 1.0
  GROUP BY
    result_id) wpps
),
_pps_120 AS (
  SELECT
    res.id result_id,
    count(pp.id) count120
  FROM
    past_performances pp
    INNER JOIN horses h ON pp.horse_id = h.id
    INNER JOIN results res ON res.horse_id = h.id
    INNER JOIN scoped_races r ON res.race_id = r.id
    INNER JOIN tracks t ON r.track_id = t.id
    INNER JOIN courses c ON c.id = r.course_id
  WHERE
    1 = 1
    AND r.date > pp.race_date
    AND r.date - 120 < pp.race_date
    AND c.distance >= 5
    AND c.distance <= 12
  GROUP BY
    result_id
),
datax AS (
  SELECT
    res.race_id,
    count(race_id) AS field_size,
  AVG(ln(cast(res.lifetime_earn AS float) + 1) / (res.lifetime_starts + 1)) avg_lifetime_eps,
  AVG(ln(cast(res.turf_earn AS float) + 1) / (res.turf_starts + 1)) avg_turf_eps,
  AVG(hpps.perf) avg_total_perf,
  AVG(hpps.beyer) avg_total_beyer,
  AVG(hpps.first_call_position) avg_total_first_call,
  AVG(hpps.second_call_position) avg_total_second_call,
  AVG(spps.perf) avg_similar_perf,
  AVG(spps.beyer) avg_similar_beyer,
  AVG(spps.first_call_position) avg_similar_first_pos,
  AVG(spps.second_call_position) avg_similar_second_pos
FROM
  results res
  INNER JOIN races r ON res.race_id = r.id
  INNER JOIN tracks t ON r.track_id = t.id
  INNER JOIN courses c ON r.course_id = c.id
    LEFT JOIN _historical_pps hpps ON res.id = hpps.result_id
    LEFT JOIN _similar_pps spps ON res.id = spps.result_id
  WHERE
    1 = 1
    AND c.distance >= 5
    AND c.distance <= 12
    AND (res.scratched IS NULL
      OR NOT res.scratched)
  GROUP BY
    race_id
)
SELECT
  res.race_id,
  res.id AS result_id,
  res.program_number,
  h.name AS horse_name,
  rank() OVER (PARTITION BY res.race_id ORDER BY res.post_position ASC) AS post_position,
    datax.field_size,
    c.distance race_distance,
    c.surface race_surface,
    t.code race_track_code,
    r.classification race_classification,
    r.is_state_bred race_state_bred,
    r.sex_restrictions race_sex_restrictions,
    r.age_restrictions race_age_restrictions,
    r.grade race_grade,
    EXTRACT(QUARTER FROM r.date) quarter,
  h.sex horse_sex,
  res.lasix horse_lasix,
  res.blinker_change horse_blinker_change,
  ((ln(cast(res.lifetime_earn AS float) + 1) / (res.lifetime_starts + 1) - datax.avg_lifetime_eps) / 0.78) lifetime_eps,
  ((ln(cast(res.turf_earn AS float) + 1) / (res.turf_starts + 1) - datax.avg_turf_eps) / 0.78) turf_eps,
  hpps.pp_count,
  (hpps.perf - datax.avg_total_perf) / 1.52 total_perf,
  (hpps.beyer - datax.avg_total_beyer) / 0.173 total_beyer,
  (hpps.first_call_position - datax.avg_total_first_call) / 0.223 total_first_call,
  (hpps.second_call_position - datax.avg_total_second_call) / 0.223 total_second_call,
  (spps.perf - datax.avg_similar_perf) / 1.52 similar_perf,
  (spps.beyer - datax.avg_similar_beyer) / 0.173 similar_beyer,
  (spps.first_call_position - datax.avg_similar_first_pos) / 0.223 similar_first_pos,
  (spps.second_call_position - datax.avg_similar_second_pos) / 0.223 similar_second_pos,
  spps.dslr,
  CAST(res.jockey_ytd_wins AS float) / (res.jockey_ytd_starts + 1) jock,
  CAST(res.trainer_ytd_wins AS float) / (res.trainer_ytd_starts + 1) trainer,
  pp120.count120,
  CASE WHEN res.track_starts > 0 THEN
  (1.0 - 1.0 + res.track_wins + res.track_places + res.track_shows) / res.track_starts
ELSE
  0
  END track_itm,
  ln(h.stud_fee + 1) stud_fee,
  ln(h.sale_price + 1) sale_price,
  EXTRACT('year' FROM r.date) - h.year_born age
FROM
  horses h
  INNER JOIN results res ON res.horse_id = h.id
  INNER JOIN scoped_races r ON res.race_id = r.id
  INNER JOIN tracks t ON r.track_id = t.id
  INNER JOIN courses c ON r.course_id = c.id
  LEFT JOIN _historical_pps hpps ON res.id = hpps.result_id
  LEFT JOIN _similar_pps spps ON res.id = spps.result_id
  INNER JOIN datax ON r.id = datax.race_id
  LEFT JOIN _pps_120 pp120 ON res.id = pp120.result_id
WHERE
  1 = 1
  AND c.distance >= 5
  AND c.distance <= 12
  AND (res.scratched IS NULL
    OR NOT res.scratched)
