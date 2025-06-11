variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región para los recursos"
  type        = string
  default     = "us-central1"
}
