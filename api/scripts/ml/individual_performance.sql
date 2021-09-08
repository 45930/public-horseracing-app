WITH scoped_races AS (
  SELECT
    *
  FROM
    races
  WHERE
    date = {{date_input}}
),
e_stats AS (
  SELECT
    res.race_id,
    res.horse_id,
    CASE WHEN res.lifetime_starts > 0 THEN
      ROUND(LN((res.lifetime_earn / res.lifetime_starts) + 1), 4)
    END AS eps,
    CASE WHEN res.lifetime_starts > 0 THEN
      ROUND(CAST(res.lifetime_wins AS numeric) / res.lifetime_starts, 4)
    END AS win_rate,
    CASE WHEN res.turf_starts > 0 THEN
      ROUND(LN((res.turf_earn / res.turf_starts) + 1), 4)
    END AS turf_eps,
    CASE WHEN res.turf_starts > 0 THEN
      ROUND(CAST(((((res.turf_wins * 1.2) + (res.turf_places * 0.8)) / res.turf_starts) - 0.35) * LN(res.turf_starts + 1) AS numeric), 4)
    END AS turf_win_factor,
    CASE WHEN res.distance_starts > 0 THEN
      ROUND(LN((res.distance_earn / res.distance_starts) + 1), 4)
    END AS distance_eps,
    CASE WHEN res.distance_starts > 0 THEN
      ROUND(CAST(((((res.distance_wins * 1.2) + (res.distance_places * 0.8)) / res.distance_starts) - 0.35) * LN(res.distance_starts + 1) AS numeric), 4)
    END AS distance_win_factor,
    CASE WHEN res.track_starts > 0 THEN
      ROUND(LN((res.track_earn / res.track_starts) + 1), 4)
    END AS track_eps,
    CASE WHEN res.track_starts > 0 THEN
      ROUND(CAST(((((res.track_wins * 1.2) + (res.track_places * 0.8)) / res.track_starts) - 0.35) * LN(res.track_starts + 1) AS numeric), 4)
    END AS track_win_factor,
    CASE WHEN res.fast_dirt_starts > 0 THEN
      ROUND(LN((res.fast_dirt_earn / res.fast_dirt_starts) + 1), 4)
    END AS fast_dirt_eps,
    CASE WHEN res.fast_dirt_starts > 0 THEN
      ROUND(CAST(((((res.fast_dirt_wins * 1.2) + (res.fast_dirt_places * 0.8)) / res.fast_dirt_starts) - 0.35) * LN(res.fast_dirt_starts + 1) AS numeric), 4)
    END AS fast_dirt_win_factor
  FROM
    results res
    INNER JOIN scoped_races ra ON res.race_id = ra.id
),
ppl AS (
  SELECT
    pp.id AS pp_id,
    res.race_id,
    res.horse_id,
    rank() OVER (PARTITION BY res.race_id,
      res.horse_id ORDER BY pp.beyer_or_foreign_speed DESC) AS pp_speed_rank,
    rank() OVER (PARTITION BY res.race_id,
      res.horse_id ORDER BY pp.race_date DESC) AS pp_line_rank,
    pp.beyer_or_foreign_speed,
    pp.distance,
    pp.purse,
    pp.race_date,
    CASE WHEN pp.claimed_code = 'c' THEN
      1
    ELSE
      0
    END AS claimed,
    (2 - ((CAST(pp.final_call_position AS DECIMAL) / pp.field_size) + LEAST (
        CASE WHEN pp.final_call_position > 1 THEN
          pp.final_call_lengths_back
        ELSE
          0.0
        END / 2 * (pp.distance), 1))) AS comprehensive_perf
  FROM
    results res
    INNER JOIN scoped_races ra ON res.race_id = ra.id
    INNER JOIN past_performances pp ON pp.horse_id = res.horse_id
  WHERE
    pp.race_date < ra.date
    AND pp.beyer_or_foreign_speed < 200
    AND pp.beyer_or_foreign_speed > 0
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
pp120 AS (
  SELECT
    pp.id AS pp_id,
    res.race_id,
    res.horse_id,
    pp.beyer_or_foreign_speed,
    1 AS race_sum
  FROM
    results res
    INNER JOIN scoped_races ra ON res.race_id = ra.id
    INNER JOIN past_performances pp ON pp.horse_id = res.horse_id
  WHERE
    pp.race_date >= ra.date - interval '120 DAY'
    AND pp.race_date < ra.date
    AND pp.beyer_or_foreign_speed < 200
    AND pp.beyer_or_foreign_speed > 0
),
pp_agg AS (
  SELECT
    ppl.race_id,
    ppl.horse_id,
    COUNT(ppl.*) AS count_races_lifetime,
    MAX(ppl.beyer_or_foreign_speed) AS best_speed_lifetime,
  ROUND(AVG(ppl.beyer_or_foreign_speed), 4) AS avg_speed_lifetime,
  ROUND(AVG(ppl.comprehensive_perf), 4) AS comprehensive_perf,
  MIN(ppl.distance) AS min_distance_raced,
  MAX(ppl.distance) AS max_distance_raced,
  MAX(ppl.race_date) AS most_recent_race_date
FROM
  ppl
GROUP BY
  ppl.race_id,
  ppl.horse_id
),
pp365_agg AS (
  SELECT
    pp365.race_id,
    pp365.horse_id,
    MAX(pp365.beyer_or_foreign_speed) AS best_speed_365,
    ROUND(AVG(pp365.beyer_or_foreign_speed), 4) AS avg_speed_365,
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
),
pp120_agg AS (
  SELECT
    pp120.race_id,
    pp120.horse_id,
    SUM(pp120.race_sum) AS count_races_120,
    MAX(pp120.beyer_or_foreign_speed) AS best_speed_120
  FROM
    pp120
  GROUP BY
    pp120.race_id,
    pp120.horse_id
),
pp_last_3 AS (
  SELECT
    race_id,
    horse_id,
    ROUND(AVG(LN(purse + 1)), 4) AS purse_3,
    MAX(claimed) AS claimed_3
  FROM
    ppl
  WHERE
    pp_line_rank <= 3
  GROUP BY
    race_id,
    horse_id
),
pp_best_3 AS (
  SELECT
    race_id,
    horse_id,
    ROUND(AVG(beyer_or_foreign_speed), 4) AS best_speed_3
  FROM
    ppl
  WHERE
    pp_speed_rank <= 3
  GROUP BY
    race_id,
    horse_id
),
pp_stats AS (
  SELECT
    pp_agg.race_id,
    pp_agg.horse_id,
    pp_agg.count_races_lifetime,
    pp_agg.best_speed_lifetime,
    pp_agg.avg_speed_lifetime,
    pp_agg.comprehensive_perf,
    pp_agg.min_distance_raced,
    pp_agg.max_distance_raced,
    pp_agg.most_recent_race_date,
    pp365_agg.best_speed_365,
    pp365_agg.avg_speed_365,
    pp365_agg.pace,
    pp365_agg.runstyle,
    pp120_agg.count_races_120,
    pp120_agg.best_speed_120,
    pp_last_3.purse_3,
    pp_last_3.claimed_3,
    pp_best_3.best_speed_3
  FROM
    pp_agg
    INNER JOIN pp_last_3 ON pp_agg.horse_id = pp_last_3.horse_id
      AND pp_agg.race_id = pp_last_3.race_id
    INNER JOIN pp_best_3 ON pp_agg.horse_id = pp_best_3.horse_id
      AND pp_agg.race_id = pp_best_3.race_id
    LEFT JOIN pp365_agg ON pp_agg.horse_id = pp365_agg.horse_id
      AND pp_agg.race_id = pp365_agg.race_id
    LEFT JOIN pp120_agg ON pp_agg.horse_id = pp120_agg.horse_id
      AND pp_agg.race_id = pp120_agg.race_id
),
stats AS (
  SELECT
    res.id AS result_id,
    res.race_id AS key_race_id, -- es.* and pp.* include these fields
    res.horse_id AS key_horse_id,
    h.name AS horse_name,
    res.program_number,
    res.post_position,
    EXTRACT(YEAR FROM ra.date) - h.year_born AS age,
    CASE EXTRACT(YEAR FROM ra.date) - h.year_born
    WHEN 3 THEN
      1
    ELSE
      0
    END AS three_yo,
    CASE EXTRACT(YEAR FROM ra.date) - h.year_born
    WHEN 4 THEN
      1
    ELSE
      0
    END AS four_yo,
    h.sex,
    CASE WHEN h.sex IN ('g', 'h', 'c', 'r') THEN
      1
    ELSE
      0
    END AS male,
    es.eps,
    es.win_rate,
    es.turf_eps,
    es.turf_win_factor,
    es.distance_eps,
    es.distance_win_factor,
    es.track_eps,
    es.track_win_factor,
    es.fast_dirt_eps,
    es.fast_dirt_win_factor,
    pp.count_races_lifetime,
    pp.best_speed_lifetime,
    pp.avg_speed_lifetime,
    pp.comprehensive_perf,
    pp.min_distance_raced,
    pp.max_distance_raced,
    pp.most_recent_race_date,
    pp.best_speed_365,
    pp.avg_speed_365,
    pp.pace,
    pp.runstyle,
    pp.count_races_120,
    pp.best_speed_120,
    pp.purse_3,
    pp.claimed_3,
    pp.best_speed_3,
    ra.date - pp.most_recent_race_date AS dslr
  FROM
    scoped_races ra
  INNER JOIN results res ON ra.id = res.race_id
  INNER JOIN horses h ON h.id = res.horse_id
  INNER JOIN e_stats es ON res.race_id = es.race_id
    AND res.horse_id = es.horse_id
  LEFT JOIN pp_stats pp ON res.race_id = pp.race_id
    AND res.horse_id = pp.horse_id
  WHERE (res.scratched IS NULL
    OR NOT res.scratched)
),
race_averages AS (
  SELECT
    key_race_id AS race_id,
    AVG(best_speed_lifetime) AS avg_best_speed_lifetime,
  AVG(avg_speed_lifetime) AS avg_avg_speed_lifetime,
  AVG(comprehensive_perf) AS avg_comprehensive_perf,
  AVG(best_speed_365) AS avg_best_speed_365,
  AVG(avg_speed_365) AS avg_avg_speed_365,
  AVG(purse_3) AS avg_purse_3,
  AVG(best_speed_3) AS avg_best_speed_3,
  AVG(eps) AS avg_eps,
  MAX(male) AS male_in_race,
  MAX(three_yo) AS three_yo_in_race,
  MAX(four_yo) AS four_yo_in_race,
  COUNT(*) AS field_size
FROM
  stats
GROUP BY
  key_race_id
),
prediction_data AS (
  SELECT
    s.key_race_id AS race_id,
    s.key_horse_id AS horse_id,
    s.result_id,
    s.horse_name,
    s.program_number,
    s.post_position,
    s.win_rate,
    r_avg.field_size,
    ROUND((s.best_speed_lifetime - r_avg.avg_best_speed_lifetime) / (
      SELECT
        stdev_best_speed_lifetime FROM _stdevs), 4) AS rel_best_speed_lifetime,
  ROUND((s.avg_speed_lifetime - r_avg.avg_avg_speed_lifetime) / (
    SELECT
      stdev_avg_speed_lifetime FROM _stdevs), 4) AS rel_avg_speed_lifetime,
ROUND((s.comprehensive_perf - r_avg.avg_comprehensive_perf) / (
  SELECT
    stdev_comprehensive_perf FROM _stdevs), 4) AS rel_comprehensive_perf,
ROUND((s.best_speed_365 - r_avg.avg_best_speed_365) / (
  SELECT
    stdev_best_speed_365 FROM _stdevs), 4) AS rel_best_speed_365,
ROUND((s.avg_speed_365 - r_avg.avg_avg_speed_365) / (
  SELECT
    stdev_avg_speed_365 FROM _stdevs), 4) AS rel_avg_speed_365,
ROUND((s.purse_3 - r_avg.avg_purse_3) / (
  SELECT
    stdev_purse_3 FROM _stdevs), 4) AS rel_purse_3,
ROUND((s.best_speed_3 - r_avg.avg_best_speed_3) / (
  SELECT
    stdev_best_speed_3 FROM _stdevs), 4) AS rel_best_speed_3,
ROUND((s.eps - r_avg.avg_eps) / (
  SELECT
    stdev_eps FROM _stdevs), 4) AS rel_eps,
s.count_races_lifetime,
s.count_races_120,
s.pace,
s.runstyle,
s.claimed_3,
CASE WHEN s.male = 0
  AND r_avg.male_in_race = 1 THEN
  1
ELSE
  0
END AS girl_against_boys,
s.age,
CASE WHEN s.age = 2
  AND (r_avg.three_yo_in_race = 1
    OR r_avg.four_yo_in_race = 1) THEN
  1
ELSE
  0
END AS two_yo_against_older,
CASE WHEN s.age = 3
  AND r_avg.four_yo_in_race = 1 THEN
  1
ELSE
  0
END AS three_yo_against_older,
s.dslr,
CASE WHEN s.dslr <= 7 THEN
  1
ELSE
  0
END AS run_this_week,
CASE WHEN s.dslr > 7
  AND s.dslr <= 30 THEN
  1
ELSE
  0
END AS run_this_month,
CASE WHEN s.dslr > 30
  AND s.dslr <= 90 THEN
  1
ELSE
  0
END AS run_this_quarter,
CASE WHEN s.dslr > 90
  AND s.dslr <= 365 THEN
  1
ELSE
  0
END AS run_this_year,
CASE WHEN s.dslr > 365 THEN
  1
ELSE
  0
END AS layoff_gt_year
FROM
  stats s
  INNER JOIN race_averages r_avg ON s.key_race_id = r_avg.race_id
)
SELECT
  td.result_id,
  td.race_id,
  td.program_number,
  ra.date,
  ra.race_number,
  ra.purse,
  ra.classification,
  c.distance,
  c.track_code,
  c.surface,
  td.horse_id,
  td.horse_name,
  td.rel_best_speed_lifetime,
  td.rel_avg_speed_lifetime,
  td.rel_comprehensive_perf,
  td.rel_best_speed_365,
  td.rel_avg_speed_365,
  td.rel_purse_3,
  td.rel_best_speed_3,
  td.rel_eps,
  td.win_rate,
  td.count_races_lifetime,
  td.count_races_120,
  td.pace,
  td.runstyle,
  td.claimed_3,
  td.girl_against_boys,
  td.three_yo_against_older,
  td.run_this_week,
  td.run_this_month,
  td.run_this_quarter,
  td.run_this_year,
  layoff_gt_year,
  CASE WHEN c.distance < 8 THEN
    1
  ELSE
    0
  END AS sprint
FROM
  scoped_races ra
  INNER JOIN prediction_data td ON ra.id = td.race_id
  INNER JOIN courses c ON ra.course_id = c.id
  INNER JOIN (
    SELECT
      race_id,
      MIN(starts) AS min_starts
    FROM (
      SELECT
        ra.id AS race_id,
        CASE WHEN count_races_lifetime IS NULL THEN
          0
        ELSE
          count_races_lifetime
        END AS starts
      FROM
        scoped_races ra
        INNER JOIN prediction_data td ON ra.id = td.race_id) ssq
    GROUP BY
      race_id) sq ON ra.id = sq.race_id
WHERE
  td.field_size > 4
  AND td.field_size < 14
  AND sq.min_starts > 0
  AND c.distance > 4
  AND c.distance <= 12
  AND c.surface IN ('a', 'd', 't', 'x')
ORDER BY
  td.race_id ASC,
  td.post_position ASC
