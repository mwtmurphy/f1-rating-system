-- noqa: disable=CP02

SELECT
  raceId AS race_id,
  year   AS race_year,
  round  AS year_round,
  date   AS race_date

FROM {{ source('source', 'races') }}
