import json
import os
from pathlib import Path

# Utilities
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

# The full path to the repository root.
BASE_DIR = PROJECT_PACKAGE.parent

# Grab secret data
try:
    with open(BASE_DIR.joinpath('config', 'secrets.json')) as secret_file:
        SECRETS = json.load(secret_file)
except IOError:
    print('Load default config')
    SECRETS = {
        'secret_key': 'qwerty',
        'db_name': 'main.sqlite3',
        'db_engine': 'django.db.backends.sqlite3',
    }

SECRET_KEY = str(SECRETS['secret_key'])

# Application definition

INSTALLED_APPS = [
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
]

ROOT_URLCONF = 'djekko.urls'

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

WSGI_APPLICATION = 'djekko.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': SECRETS.get('db_engine'),
        'NAME': SECRETS.get('db_name', ''),
        'USER': SECRETS.get('db_owner', ''),
        'HOST': SECRETS.get('db_host', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
        'PORT': SECRETS.get('db_port', ''),
    }
}

# Password validation

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
