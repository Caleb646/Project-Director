#!/bin/sh
echo "starting backend"
python /app/backend/project-director/manage.py makemigrations authentication --no-input
python /app/backend/project-director/manage.py migrate authentication --no-input
echo "successfully migrated authentication"
python /app/backend/project-director/manage.py makemigrations bid_api --no-input
python /app/backend/project-director/manage.py migrate bid_api --no-input
echo "successfully migrated bid_api"
python /app/backend/project-director/manage.py makemigrations pm_api --no-input
python /app/backend/project-director/manage.py migrate pm_api --no-input
echo "successfully migrated pm_api"
python /app/backend/project-director/manage.py makemigrations --no-input
python /app/backend/project-director/manage.py migrate --no-input
echo "successfully migrated auth and bid apis"
#setup admin accounts and test users
python /app/backend/project-director/manage.py create_test_data
echo "successfully setup test data"
python /app/backend/project-director/manage.py runserver 0.0.0.0:8000
