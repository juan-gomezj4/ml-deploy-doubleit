output "service_account_email" {
  value = google_service_account.github_deployer.email
}

output "artifact_registry_url" {
  value = "us-central1-docker.pkg.dev/${var.project_id}/ml-deploy-repo"
}
