module "test_module" {
  env         = var.env
  location    = var.location
  bucket_name = google_storage_bucket.functions_bucket.name
  environment_variables = {
    ENV               = var.env,
    LOCATION_ID       = "europe-west1",
    NAME = "test_${var.env}",
  }
  memory_mb   = 512
  timeout     = 540
}
