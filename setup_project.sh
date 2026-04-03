#!/bin/bash
set -e

echo "Application du schéma SQL..."
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/01_schema.sql
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/02_private_dashboard_views.sql
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/03_public_dashboard_views.sql
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/04_monitoring.sql
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/05_roles_and_permissions.sql
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/06_constraints.sql

echo "Synchronisation SQL terminée."
