locals {
  bq_datasets = ["source", "staging", "intermediate", "marts"]
}

# ── BigQuery datasets ─────────────────────────────────────────────────────────

resource "google_bigquery_dataset" "layers" {
  for_each   = toset(local.bq_datasets)
  dataset_id = each.key
  location   = var.region
}

# ── Streamlit service account ─────────────────────────────────────────────────

resource "google_service_account" "streamlit" {
  account_id   = "streamlit-bq-reader"
  display_name = "Streamlit BigQuery Reader"
}

resource "google_project_iam_member" "streamlit_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.streamlit.email}"
}

resource "google_bigquery_dataset_iam_member" "streamlit_viewer" {
  for_each   = toset(local.bq_datasets)
  dataset_id = google_bigquery_dataset.layers[each.key].dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${google_service_account.streamlit.email}"
}

# ── GCS bucket for Ergast API CSVs ───────────────────────────────────────────

resource "google_storage_bucket" "raw_data" {
  name                        = "mwtmurphy-f1-rating-system-ergast-api-data"
  location                    = var.region
  uniform_bucket_level_access = true

  labels = {
    source = "ergast-api"
  }
}

resource "google_storage_bucket_iam_member" "streamlit_gcs_reader" {
  bucket = google_storage_bucket.raw_data.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.streamlit.email}"
}
