select
    constructorYearId as constructor_year_id,
    constructorId as constructor_id,
    year

from {{ source('source', 'constructor_year') }}
