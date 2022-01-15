import os
from datetime import timedelta
from importlib import import_module
from pathlib import Path

from dotenv import load_dotenv

#TODO remove before dockerizing
#C:\Users\MyCod\Coding Projects\Python Projects\Project-Director\app\backend\project-director
load_dotenv(r"C:/Users/MyCod/Coding Projects/Python Projects/Project-Director/backend/project-director/.env.dev")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = bool(int(os.getenv("DEBUG", default="0")))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
FRONTEND_URL = os.getenv("FRONTEND_URL")

LOGIN_TOKEN_LENGTH = int(os.getenv("LOGIN_TOKEN_LENGTH"))

JWT_ACCESS_TOKEN_EXPIRATION = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRATION"))
JWT_REFRESH_TOKEN_EXPIRATION = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRATION"))

# SESSION_COOKIE_SECURE= False
#SESSION_COOKIE_DOMAIN= "localhost"
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
################# CORS SETTINGS #################
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = DEBUG

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err

IMPORT_STRING = import_string

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'gdstorage',

    'authentication',
    'pm_api',
    'bid_api',
    
    'rest_framework'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project-director.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project-director.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv("SQL_ENGINE"),
        'NAME': os.getenv("SQL_DATABASE"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("SQL_HOST"),
        'PORT': os.getenv("SQL_PORT")
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/django_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'django_static')

#############################JWT Setup##########################
"""
Setup link: https://hackernoon.com/110percent-complete-jwt-authentication-with-django-and-react-2020-iejq34ta
Docs Link: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
Docs Link: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
"""
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication', Add this or use access token to view schema
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        #anon is for unathenticated users
        'anon': '100/day',
        'user': '10000/day'
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRATION),
}

####################### My Models and Managers #####################################
AUTH_USER_MODEL = 'authentication.CustomUser'
TOKEN_AUTH_MODEL = 'authentication.InviteToken'
COMPANY_MODEL = 'authentication.Company'
EMAIL_MANAGER = 'authentication.managers.EmailManager'
BASE_TEST_MANAGER = 'authentication.test_managers.BaseTestManager'
####################################################################################

##########################CSRF Token Setup#########################################

CSRF_COOKIE_HTTPONLY = bool(int(os.getenv("CSRF_COOKIE_HTTPONLY", default=1)))
CSRF_COOKIE_SECURE = bool(int(os.getenv("CSRF_COOKIE_SECURE", default=1)))
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE") 
SECURE_PROXY_SSL_HEADER = os.getenv("SECURE_PROXY_SSL_HEADER", default=None)
SECURE_SSL_REDIRECT = bool(int(os.getenv("SECURE_SSL_REDIRECT", default=1)))

#################################################################


############################ File Upload Settings ################


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#############################################################


############################ Email Backend Settings ################


EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", default=False)
EMAIL_HOST = os.getenv("EMAIL_HOST", default=None)
EMAIL_PORT = os.getenv("EMAIL_PORT", default=None)
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


#############################################################

############## Google Drive Upload Settings ##################

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR, 'gdrive-secretkey.json')
#GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = '<base google drive path for file uploads>' # OPTIONAL

##############################################################

