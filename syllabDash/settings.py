"""
Django settings for syllabDash project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# import pylibmc
# from memcacheify import memcacheify

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a$=3l%wa#ts@hkzy(nfaq$k!ht(ieao9it-nektuux7ib^pvm0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'syllab-dash.herokuapp.com']

# servers = os.environ['mc5.dev.ec2.memcachier.com:11211']
# username = os.environ['8D80A8']
# password = os.environ['B9689004027E5F147242E3EE56D3AB3B']


INSTALLED_APPS = [
    'syllab_dash.apps.SyllabDashConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]



ROOT_URLCONF = 'syllabDash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'syllab_dash', 'templates')],
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

STATIC_ROOT = os.path.join(BASE_DIR, 'syllab_dash', 'static')

WSGI_APPLICATION = 'syllabDash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#CACHES = memcacheify()


CACHES = {

#     'default': {
#         # Use pylibmc
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',

#         # TIMEOUT is not the connection timeout! It's the default expiration
#         # timeout that should be applied to keys! Setting it to `None`
#         # disables expiration.
#         'TIMEOUT': 7200,

#         'LOCATION': servers,

#         'OPTIONS': {
#             # Use binary memcache protocol (needed for authentication)
#             'binary': True,
#             'username': username,
#             'password': password,
#             'behaviors': {
#                 # Enable faster IO
#                 'no_block': True,
#                 'tcp_nodelay': True,

#                 # Keep connection alive
#                 'tcp_keepalive': True,

#                 # Timeout settings
#                 'connect_timeout': 2000, # ms
#                 'send_timeout': 750 * 1000, # us
#                 'receive_timeout': 750 * 1000, # us
#                 '_poll_timeout': 2000, # ms

#                 # Better failover
#                 'ketama': True,
#                 'remove_failed': 1,
#                 'retry_timeout': 2,
#                 'dead_timeout': 30,
#             }
#         }
#     }
     'default': {
         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
         'LOCATION': 'unique-snowflake',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/syllab_dash/static/'

STATICFILE_DIRS = (
    os.path.join(BASE_DIR, 'syllab_dash', 'static', 'syllab_dash')
)
