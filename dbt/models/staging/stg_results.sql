-- noqa: disable=CP02

SELECT
    raceId AS race_id,
    constructorId AS constructor_id,
    driverId AS driver_id,
    grid,
    statusId AS status_id,
    SAFE_CAST(NULLIF(position, '\\N') AS INT64) AS position
FROM {{ source('source', 'results') }}
