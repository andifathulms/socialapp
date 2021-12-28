"""
Django settings for socialapp project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku

"""
import environ

#initialise environ
env = environ.Env()
environ.Env.read_env()
"""
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4^52@bae=edb46jzqm2-h#%9_wh5acblz=x#v=ho(98k)8_ero"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['pnptalk.herokuapp.com','127.0.0.1']

#twisted-iocpsupport==1.0.2
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'crispy_forms',
    'storages',
    'channels',
    'mathfilters',
    'rest_framework',
    'mptt',
    'django_editorjs',
    'django_htmx',

    'personal',
    'account',
    'friend',
    'public_chat',
    'chat',
    'notification',
    'post',
    'account_profile',
    'follower',
    'forum',
    'marketplace',
    'blog',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework.authentication.BasicAuthentication',
         'rest_framework.authentication.SessionAuthentication',
        #'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'socialapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custom_tags': 'post.templatetags.custom_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'socialapp.wsgi.application'
ASGI_APPLICATION = 'socialapp.routing.application'

AUTH_USER_MODEL = 'account.Account'
AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.AllowAllUsersModelBackend', 
    'account.backends.CaseInsensitiveModelBackend',
    )


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

#Notice change on production
#static config
STATICFILES_DIRS = [
    BASE_DIR/"static",
    BASE_DIR/"media", #DEV
]
STATIC_URL = '/static/'
MEDIA_URL = '/media/' #DEV
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')  #DEV
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')  #DEV

TEMP = os.path.join(BASE_DIR, 'media_cdn/temp')  #DEV
#TEMP = os.path.join(BASE_DIR, 'temp')  #PROD

BASE_URL = "http://127.0.0.1:8000"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10mb = 10 * 1024 *1024

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Dev only

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "officialandifathul@gmail.com"
EMAIL_HOST_PASSWORD = "RiemannConjecture"


#Postgres config
DB_NAME = "socialapp"
DB_USER = "afms"
DB_PASSWORD = "SteveG08"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        #'HOST': 'ec2-18-211-194-36.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
#chanel-redis config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('127.0.0.1', 6379)], #dev only
            #"hosts": [('pnptalk.herokuapp.com', 6379)],
        },
    },
}

DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
]

LOGIN_URL = '/login'

AWS_ACCESS_KEY_ID="AKIAXSGIDQGEESDBZHGJ"
AWS_SECRET_ACCESS_KEY="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"
AWS_STORAGE_BUCKET_NAME="django-pnp-talk"

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
django_heroku.settings(locals())