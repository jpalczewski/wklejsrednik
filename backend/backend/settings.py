"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


# Standard Library
import os
from datetime import timedelta
from distutils.debug import DEBUG
from pathlib import Path

# 3rd-Party
import dj_email_url
import environ
from configurations import Configuration, values

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


class Common(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = values.SecretValue(environ_name='SECRET_KEY', environ_prefix=None)

    DEBUG = True

    ALLOWED_HOSTS = ['backend', 'localhost']

    INSTALLED_APPS = [
        'users',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "graphene_django",
        'pastes',
        'reports',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        "whitenoise.middleware.WhiteNoiseMiddleware",
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]

    GRAPHENE = {
        "SCHEMA": "schema.schema_v1",
        "MIDDLEWARE": [
            "graphql_jwt.middleware.JSONWebTokenMiddleware",
            "graphene_django.debug.DjangoDebugMiddleware",
        ],
    }

    AUTHENTICATION_BACKENDS = [
        "graphql_jwt.backends.JSONWebTokenBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]

    GRAPHQL_JWT = {
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_EXPIRATION_DELTA": timedelta(minutes=7),
        "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=4),
    }

    ROOT_URLCONF = 'backend.urls'

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

    WSGI_APPLICATION = 'backend.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    AUTH_USER_MODEL = 'users.User'
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

    LANGUAGE_CODE = 'pl-pl'

    TIME_ZONE = 'Europe/Warsaw'

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = 'static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


class Dev(Common):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    if os.environ.get('EMAIL_URL') is not None:
        email_config = dj_email_url.config()
        EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
        EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
        EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
        EMAIL_HOST = email_config['EMAIL_HOST']
        EMAIL_PORT = email_config['EMAIL_PORT']
        EMAIL_BACKEND = email_config['EMAIL_BACKEND']
        EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
        EMAIL_USE_SSL = email_config['EMAIL_USE_SSL']
        EMAIL_TIMEOUT = email_config['EMAIL_TIMEOUT']

    if os.environ.get('DATABASE_URL') is not None:
        DATABASES = {
            'default': env.db(),
        }

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(Common.BASE_DIR, 'media/')

    LOGGING = {
        'version': 1,  # the dictConfig format version
        'disable_existing_loggers': False,  # retain the default loggers
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'console-fmt': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard3',
            },
            # 'file': {
            #     'level': 'DEBUG',
            #     'class': 'logging.FileHandler',
            #     'filename': 'debug.log',
            # },
        },
        'formatters': {
            'standard3': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s[:%(lineno)d]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'standard2': {
                'format': '%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s'
            },
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'root': {'handlers': ['console-fmt'], 'level': 'DEBUG'},
        'level': 'DEBUG',
    }
    CELERY_TIMEZONE = "Europe/Warsaw"
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'django_extensions',
    ]

    ATTACHMENT_TIMESPAN = values.IntegerValue(
        environ_name="ATTACHMENT_TIMESPAN", environ_prefix=None, default=300
    )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


class Prod(Common):
    DEBUG = False

    ALLOWED_HOSTS = ['proxy', 'backend']


class CI(Common):

    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    email_config = ''
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': values.Value(
                'semipaste', environ_name='POSTGRES_DB', environ_prefix=None
            ),
            'USER': values.Value(
                'postgres', environ_name='POSTGRES_USER', environ_prefix=None
            ),
            'PASSWORD': values.Value(
                'password', environ_name='POSTGRES_PASSWORD', environ_prefix=None
            ),
            'HOST': values.Value(
                'db', environ_name='POSTGRES_HOST', environ_prefix=None
            ),
            'PORT': 5432,
        }
    }
