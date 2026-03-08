SELECT
    ra.race_year,
    ra.round,
    ra.date,
    re.constructor_id,
    cy.constructor_year_id,
    re.driver_id,
    re.grid,
    re.position,
    re.status_id
FROM {{ ref('stg_races') }} AS ra
INNER JOIN {{ ref('stg_results') }} AS re
    ON ra.race_id = re.race_id
LEFT JOIN {{ ref('stg_constructor_year') }} AS cy
    ON
        re.constructor_id = cy.constructor_id
        AND ra.race_year = cy.race_year
ORDER BY ra.race_year, ra.round, re.position, re.grid
