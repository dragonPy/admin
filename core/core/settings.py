"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
from django.utils.translation import ugettext_lazy as _

IS_ADMIN = os.environ['IS_ADMIN']

# For Testing Environment
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123809fkjl129sdf09/@#123sdf012!@#SDF'

APPEND_SLASH = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ['DEBUG'])

if DEBUG:
    ALLOWED_HOSTS = ['localhost','127.0.0.1']
else:
    ALLOWED_HOSTS = ['47.90.36.8'] if IS_ADMIN else ['10.24.186.245']

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = 0    

TASTYPIE_DEFAULT_FORMATS = ['json']

# Application definition

INSTALLED_APPS = [
    'suit',
    'users.apps.UsersConfig',
    'core_settings.apps.SettingsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'django_rq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

SUIT_CONFIG = {
    'ADMIN_NAME': 'VAULTECH',
    'MENU': (
        'sites',
        {'app': 'auth', 'label': _('Admin Users'), 'icon':'icon-lock'},
        {'app': 'core_settings'},
        {'app': 'users'},
    ),
}

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if DEBUG:
    db = 'testdb.sqlite3'
else:
    db = os.environ['DB_PATH']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Django Redis Queue Configurations
RQ_QUEUES = {
    'mail': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']