select
    raceId as race_id,
    constructorId as constructor_id,
    driverId as driver_id,
    grid,
    safe_cast(nullif(position, '\\N') as float64) as position,
    statusId as status_id
from {{ source('source', 'results') }}
