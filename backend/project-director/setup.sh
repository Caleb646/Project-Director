#!/bin/bash
source C:/Users/MyCod/"Coding Projects"/"Python Projects"/Project-Director/app/env/Scripts/activate
python manage.py makemigrations pm_api --no-input
python manage.py migrate pm_api --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py create_test_data