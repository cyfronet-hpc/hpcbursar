"""
Django settings for hpcbursar project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a=(_+dl$t&+(qr=42&ur2up_yhlrbxh4z&#x^(3xc=l-k3=5km'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'grantstorage'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hpcbursar.urls'

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

WSGI_APPLICATION = 'hpcbursar.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ['127.0.0.1', 'slurm01.ares.cyfronet.pl']

GRID_CERTIFICATE_LOCATION = 'path to your .pem file'
GRID_KEY_LOCATION = 'path to your .key file'

PLGRID_PORTAL_URL = 'https://portal.plgrid.pl/'
PLGRID_SITE_NAME = 'CYFRONET-ARES'

PLG_LOGIN_PREFIX = 'plg'
PLG_ACCOUNT_PREFIX = 'plg'

SLURM_CLUSTER_NAME = 'ares'
SLURM_CLIENT_VERBOSE = True
SLURM_SACCTMGR_LOCATION = '/opt/slurm/releases/production/bin/sacctmgr'
SLURM_SCONTROL_LOCATION = '/opt/slurm/releases/production/bin/scontrol'

SLURM_SUPPORTED_RESOURCES = ['CPU', 'GPU']
SLURM_RESOURCE_PARTITION_MAPPING = {
    'CPU': 'plgrid',
    'GPU': 'plgrid-gpu-v100'
}
SLURM_ACL_PLACEHOLDER = 'hpcb'

SLURM_ADMIN_USER = 'admin user'

# overwriting settings with default ones
from hpcbursar.local_settings import *
