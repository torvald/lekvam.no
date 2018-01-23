"""
Django settings for lekvam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from secret import DJANGO_KEY
SECRET_KEY = DJANGO_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'webcam',
    'wiki_wrapper',
    'todo',
    'oppskrifter',
    'stats'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lekvam.urls'

WSGI_APPLICATION = 'lekvam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

from secret import LEKVAM_DJANGO_PASSWD

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lekvam_django',
        'USER': 'lekvam_django',
        'PASSWORD': LEKVAM_DJANGO_PASSWD,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# postgres=# CREATE DATABASE lekvam_django  
# postgres-# ;  
# CREATE DATABASE  
# postgres=# CREATE USER lekvam_django WITH PASSWORD 'lol';  
# CREATE ROLE
# postgres=# ALTER ROLE lekvam_django SET client_encoding TO 'utf8';
# ALTER ROLE
# postgres=# ALTER ROLE lekvam_django SET default_transaction_isolation TO 'read committed';
# ALTER ROLE
# postgres=# GRANT ALL PRIVILEGES ON DATABASE lekvam_django To lekvam_django;
# GRAN

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

LOGOUT_REDIRECT_URL="/"
LOGIN_REDIRECT_URL="/"

LOGIN_URL="/login/"
MEDIA_ROOT='collectstatic/'
MEDIA_URL='https://lekvam.no/static/'

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/lekvam/collectstatic'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common/static'),
    os.path.join(BASE_DIR, 'wiki_wrapper/static'),
    os.path.join(BASE_DIR, 'webcam/static'),
    os.path.join(BASE_DIR, 'oppskrifter/static'),
    os.path.join(BASE_DIR, 'todo/static'),
    os.path.join(BASE_DIR, 'uploads'),
)
