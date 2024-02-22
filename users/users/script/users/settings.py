
from pathlib import Path
import os
from datetime import timedelta
import hvac

#from app.models import User

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!by_b!m3kd+$89x7#_wp7ye(5$p)66%3fc(1e-=r&nd^ukc7_)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["api.localhost", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'users.urls'

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

WSGI_APPLICATION = 'users.wsgi.application'


AUTH_USER_MODEL="users.User"

VAULT_ADDR = 'http://vault:8200'
fd = os.open("/opt/token", os.O_RDONLY)
n_bytes = 95 # token size
TOKEN = os.read(fd, n_bytes)

vault_client = hvac.Client(url='http://vault:8200', token=TOKEN)

secret_key = vault_client.read('kv/django_secrets')

SECRET_KEY = secret_key['data']['django_key']

database_credentials = vault_client.read('database/creds/my-rolev1')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': database_credentials['data']['username'],
        'PASSWORD': database_credentials['data']['password'],
        'HOST': 'postgres_users',
        'PORT': '5432',
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
#STATICFILES_DIRS = [ os.path.join(BASE_DIR,'app/static') ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTIFICATION_CLASSES': (
        'authenticate.CustomAuthentication',
    ),
}

CORS_ALLOW_CREDENTIALS = True
#CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE_FORCE_ALL = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ORIGIN_WHITELIST = [
    'https://localhost',
    'https://django_users:8001',
    'https://api.localhost',
]

CSRF_TRUSTED_ORIGINS = [
    'https://localhost',
    'https://django_users:8001',
    'https://api.localhost',
]



from datetime import timedelta
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
  'ROTATE_REFRESH_TOKENS': False,
  'BLACKLIST_AFTER_ROTATION': True,
  'UPDATE_LAST_LOGIN': False,

  'ALGORITHM': 'HS256',
  'SIGNING_KEY': SECRET_KEY,
  'VERIFYING_KEY': None,
  'AUDIENCE': None,
  'ISSUER': None,

  'AUTH_HEADER_TYPES': ('Bearer',),
  'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
  'USER_ID_FIELD': 'id',
  'USER_ID_CLAIM': 'user_id',
  'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

  'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
  'TOKEN_TYPE_CLAIM': 'token_type',

  'JTI_CLAIM': 'jti',

  'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
  'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
  'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

  # custom
  'AUTH_COOKIE': 'refresh_token',  # Cookie name. Enables cookies if value is set.
  'AUTH_COOKIE_DOMAIN': 'localhost',     # A string like "example.com", or None for standard domain cookie.
  'AUTH_COOKIE_SECURE': True,    # Whether the auth cookies should be secure (https:// only).
  'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
  'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
  'AUTH_COOKIE_SAMESITE': 'None',  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}