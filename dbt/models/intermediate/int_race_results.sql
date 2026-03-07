select
    r.year,
    r.round,
    r.date,
    res.constructor_id,
    coalesce(cy.constructor_year_id, res.constructor_id) as constructor_year_id,
    res.driver_id,
    res.grid,
    res.position,
    res.status_id
from {{ ref('stg_races') }} as r
inner join {{ ref('stg_results') }} as res on r.race_id = res.race_id
left join {{ ref('stg_constructor_year') }} as cy
    on res.constructor_id = cy.constructor_id
    and r.year = cy.year
order by r.year, r.round, res.position, res.grid
