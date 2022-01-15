CALL C:/Users/MyCod/"Coding Projects"/"Python Projects"/Project-Director/env/Scripts/activate.bat
CALL python manage.py makemigrations pm_api --no-input
CALL python manage.py migrate pm_api --no-input
CALL python manage.py makemigrations --no-input
CALL python manage.py migrate --no-input
CALL python manage.py create_test_data