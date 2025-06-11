.PHONY: help install_env test test_verbose test_coverage pre-commit_update clean_env check lint \
        terraform_init terraform_apply create_key set_gh_secret clean_key

####---- Entorno ----####

install_env: ## Instala dependencias con UV y configura pre-commit
	@echo "🚀 Syncing environment using UV and .python-version"
	uv sync --all-groups
	@echo "✅ Environment ready"
	@echo "🚀 Installing pre-commit hooks..."
	uv run pre-commit install

clean_env: ## Elimina el entorno virtual .venv
	@echo "🧹 Cleaning environment"
	@[ -d .venv ] && rm -rf .venv || echo "⚠️ .venv directory does not exist"

####---- Tests ----####

test: ## Ejecuta pruebas con cobertura
	@echo "🚀 Running tests with coverage"
	uv run pytest --cov

test_verbose: ## Ejecuta pruebas en modo detallado
	uv run pytest -v --no-header --cov

test_coverage: ## Genera reporte de cobertura XML
	uv run pytest --cov --cov-report=xml:coverage.xml

####---- Pre-commit ----####

check: ## Ejecuta todos los hooks de pre-commit
	uv run pre-commit run --all-files

lint: ## Ejecuta sólo Ruff (linting)
	uv run pre-commit run ruff

pre-commit_update: ## Actualiza los hooks de pre-commit
	uv run pre-commit clean
	uv run pre-commit autoupdate

####---- Terraform Infraestructura ----####

terraform_init: ## Inicializa Terraform en la carpeta iac
	cd iac && terraform init

terraform_apply: ## Aplica Terraform (crea recursos en GCP)
	cd iac && terraform apply -auto-approve

create_key: ## Crea clave JSON para cuenta de servicio
	gcloud iam service-accounts keys create github-creds.json \
		--iam-account=$$SA_NAME@$$PROJECT_ID.iam.gserviceaccount.com

set_gh_secret: ## Sube clave como secreto a GitHub
	gh secret set GCP_CREDENTIALS < github-creds.json

clean_key: ## Borra clave local
	rm -f github-creds.json

####---- Ayuda ----####

help: ## Muestra esta ayuda
	@printf "%-30s %s\n" "Target" "Description"
	@printf "%-30s %s\n" "-----------------------" "----------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
