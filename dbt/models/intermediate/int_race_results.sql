SELECT
  ra.race_id,
  cy.constructor_year_id,
  re.constructor_id,
  re.driver_id,
  re.race_status_id,
  ra.race_year,
  ra.year_round,
  ra.race_date,
  re.driver_start_position,
  re.driver_end_position

FROM {{ ref('stg_ergast__races') }}                   AS ra
  INNER JOIN {{ ref('stg_ergast__race_results') }}  AS re ON ra.race_id = re.race_id
  LEFT JOIN {{ ref('stg_ergast__constructor_year') }} AS cy ON re.constructor_id = cy.constructor_id
                                                               AND ra.race_year = cy.race_year
ORDER BY race_year, year_round, driver_end_position, driver_start_position
