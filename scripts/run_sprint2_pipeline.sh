#!/usr/bin/env bash
set -euo pipefail

echo "Starting PostgreSQL..."
docker compose up -d postgres

echo "Downloading MTA tax debts CSV..."
docker compose run --rm pipeline python scripts/download_mta_tax_debts.py

echo "Loading MTA tax debts into PostgreSQL raw table..."
docker compose run --rm pipeline python scripts/load_mta_tax_debts_raw.py

echo "Running dbt transformations..."
docker compose run --rm dbt dbt run --project-dir dbt_project --profiles-dir dbt_project

echo "Sprint 2 pipeline completed successfully."
echo "Start dashboard with:"
echo "docker compose up dashboard"
echo "Then open: http://localhost:8501"
