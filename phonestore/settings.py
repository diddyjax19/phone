from pathlib import Path
import os
import environ
import django_heroku
from decouple import config
from dotenv import load_dotenv
if os.path.isfile('env.py'):
     import env

# initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')
# DEBUG = True

ALLOWED_HOSTS = ['nestit-d6952187268f.herokuapp.com', 'localhost','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'store',
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

ROOT_URLCONF = 'phonestore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_preprocessors.store_menu',
                'store.context_preprocessors.cart_menu',
            ],
        },
    },
]


WSGI_APPLICATION = 'phonestore.wsgi.application'



# SQLite Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd9791vc80i44pf',
#         'USER': 'tdbotopscjtwkj',
#         'PASSWORD': '5fb28e61337775738df362ea5489fe037c0e0bee8cffde67a34289d5e660c499',
#         'HOST': 'ec2-34-242-199-141.eu-west-1.compute.amazonaws.com',  # Set to your database host
#         'PORT': '5432',       # Default PostgreSQL port
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': 'ec2-34-242-199-141.eu-west-1.compute.amazonaws.com',  # Set to your database host
        'PORT': '5432',       # Default PostgreSQL port
    }
}

# DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
#              }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

# DATABASES = {
#      'default': dj_database_url.parse(os.environ.get("postgres://tdbotopscjtwkj:5fb28e61337775738df362ea5489fe037c0e0bee8cffde67a34289d5e660c499@ec2-34-242-199-141.eu-west-1.compute.amazonaws.com:5432/d9791vc80i44pf"))
#  }

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'phonestore/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
django_heroku.settings(locals()) # Automatically Created on Production

# Settings for Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
