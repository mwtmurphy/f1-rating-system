select
    raceId as race_id,
    year,
    round,
    date
from {{ source('source', 'races') }}
