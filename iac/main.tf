provider "google" {
  project = var.project_id
  region  = var.region
}

# Cuenta de servicio
resource "google_service_account" "github_deployer" {
  account_id   = "github-deployer"
  display_name = "CI/CD deployer for GitHub Actions"
}

# Roles necesarios
resource "google_project_iam_member" "run_admin" {
  project = var.project_id
  role   = "roles/run.admin"
  member = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "artifact_admin" {
  project = var.project_id
  role   = "roles/artifactregistry.admin"
  member = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "sa_user" {
  project = var.project_id
  role   = "roles/iam.serviceAccountUser"
  member = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "cloudbuild_editor" {
  project = var.project_id
  role   = "roles/cloudbuild.builds.editor"
  member = "serviceAccount:${google_service_account.github_deployer.email}"
}

# Crear repositorio en Artifact Registry
resource "google_artifact_registry_repository" "ml_deploy_repo" {
  location      = var.region
  repository_id = "ml-deploy-repo"
  format        = "DOCKER"
  description   = "Repo para despliegue de contenedores del modelo DoubleIt"
}
