-- noqa: disable=CP02

SELECT
  statusId      AS status_id,
  LOWER(status) AS driver_status

FROM {{ source('source', 'status') }}
