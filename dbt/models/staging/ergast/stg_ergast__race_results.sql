-- noqa: disable=CP02

SELECT
  raceId                                      AS race_id,
  constructorId                               AS constructor_id,
  driverId                                    AS driver_id,
  statusId                                    AS race_status_id,
  grid                                        AS driver_start_position,
  SAFE_CAST(NULLIF(position, '\\N') AS INT64) AS driver_end_position

FROM {{ source('source', 'results') }}
