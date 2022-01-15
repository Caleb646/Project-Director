#!/bin/sh
echo "starting backend"
python manage.py makemigrations authentication --no-input
python manage.py migrate authentication --no-input
echo "successfully migrated authentication"
python manage.py makemigrations bid_api --no-input
python manage.py migrate bid_api --no-input
echo "successfully migrated bid_api"
python manage.py makemigrations pm_api --no-input
python manage.py migrate pm_api --no-input
echo "successfully migrated pm_api"
python manage.py makemigrations --no-input
python manage.py migrate --no-input
echo "successfully migrated auth and bid apis"
#setup admin accounts and test users
python manage.py create_test_data
echo "successfully setup test data"
python manage.py collectstatic --no-input
echo "successfully collected static"
uwsgi --socket=127.0.0.1:8000 --module=project-director.wsgi:application --env DJANGO_SETTINGS_MODULE=project-director.settings --master --processes=4 --threads=2
echo "successfully configured uwsgi"
#gunicorn project-director.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug