#!/bin/bash

set -e  # Falla si hay error
set -a  # Exporta automáticamente las vars del .env

# Cargar variables de entorno
source .env
set +a

# Inicializar y aplicar Terraform
make terraform_init
make terraform_apply

# Crear clave y subirla como secreto
make create_key
make set_gh_secret
make clean_key
