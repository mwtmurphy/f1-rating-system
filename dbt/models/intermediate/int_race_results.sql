-- noqa: disable=CP02

WITH base AS (
    SELECT
        ra.race_id,
        re.constructor_id,
        re.driver_id,
        ra.race_year,
        ra.year_round,
        ra.race_date,
        rs.driver_status_group,
        COALESCE(cy.constructor_year_id, re.constructor_id)
            AS constructor_year_id,
        ROW_NUMBER() OVER (
            PARTITION BY ra.race_id ORDER BY re.driver_start_position
        ) AS map_position

    FROM {{ ref('stg_ergast__races') }} AS ra
    INNER JOIN
        {{ ref('stg_ergast__race_results') }} AS re
        ON ra.race_id = re.race_id
    LEFT JOIN {{ ref('stg_ergast__constructor_year') }} AS cy
        ON
            re.constructor_id = cy.constructor_id
            AND ra.race_year = cy.race_year
    LEFT JOIN {{ ref('stg_ergast__race_statuses') }} AS rs
        ON re.race_status_id = rs.status_id
)

SELECT
    CONCAT(CAST(race_id AS STRING), '_', driver_id) AS race_result_id,
    race_id,
    constructor_year_id,
    constructor_id,
    driver_id,
    race_year,
    year_round,
    race_date,
    map_position,
    driver_status_group AS race_status,
    CASE map_position
        WHEN 1 THEN 25
        WHEN 2 THEN 18
        WHEN 3 THEN 15
        WHEN 4 THEN 12
        WHEN 5 THEN 10
        WHEN 6 THEN 8
        WHEN 7 THEN 6
        WHEN 8 THEN 4
        WHEN 9 THEN 2
        WHEN 10 THEN 1
        ELSE 0
    END AS map_points

FROM base
ORDER BY race_year, year_round, map_position
