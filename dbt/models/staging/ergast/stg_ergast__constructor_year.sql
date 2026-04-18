-- noqa: disable=CP02

SELECT
    constructorId AS constructor_id,
    year AS race_year,
    COALESCE(constructorYearId, constructorId) AS constructor_year_id

FROM {{ source('source', 'constructor_year') }}
