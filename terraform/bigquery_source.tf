locals {
  source_tables = toset([
    "circuits",
    "constructor_results",
    "constructor_standings",
    "constructor_year",
    "constructors",
    "driver_standings",
    "drivers",
    "lap_times",
    "pit_stops",
    "qualifying",
    "races",
    "results",
    "seasons",
    "sprint_results",
    "status",
  ])
}

resource "google_bigquery_table" "source" {
  for_each            = local.source_tables
  dataset_id          = google_bigquery_dataset.layers["source"].dataset_id
  table_id            = each.key
  deletion_protection = false

  external_data_configuration {
    source_uris   = ["gs://${google_storage_bucket.raw_data.name}/${each.key}.csv"]
    source_format = "CSV"
    autodetect    = true

    csv_options {
      quote             = "\""
      skip_leading_rows = 1
    }
  }
}
