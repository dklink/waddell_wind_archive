# Variables (set from .env)
variable "gcp_project_id" {
  description = "The Google Cloud project ID"
  type        = string
  sensitive   = true
}

variable "gcs_bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
}

variable "postgres_instance_name" {
  description = "The name of the PostgreSQL instance"
  type        = string
}

variable "postgres_user_name" {
  description = "The name of the PostgreSQL user"
  type        = string
}

variable "postgres_password" {
  description = "The password for the PostgreSQL user"
  type        = string
  sensitive   = true
}

variable "frontend_bucket_name" {
    description = "The name of the frontend bucket"
    type        = string 
}

# Provider definition
provider "google" {
  project = var.gcp_project_id
  region  = "us-central1"
}

# GCS Bucket Setup
resource "google_storage_bucket" "image_archive" {
  name          = var.gcs_bucket_name
  location      = "US-CENTRAL1"
  storage_class = "STANDARD"
}

# PostgreSQL Instance Setup
resource "google_sql_database_instance" "postgres_instance" {
  name             = var.postgres_instance_name
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier              = "db-f1-micro"  # Always Free Tier
    backup_configuration {
      enabled = true
    }
  }
}

resource "google_sql_user" "default_user" {
  name     = var.postgres_user_name
  password = var.postgres_password
  instance = google_sql_database_instance.postgres_instance.name
}

# Frontend Bucket Setup
resource "google_storage_bucket" "frontend_bucket" {
  name          = var.frontend_bucket_name
  location      = "us-central1"

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "frontend_public_access" {
  bucket = google_storage_bucket.frontend_bucket.name
  role   = "roles/storage.objectViewer"

  members = [
    "allUsers"
  ]
}
