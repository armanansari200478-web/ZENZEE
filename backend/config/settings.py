"""
Django settings for ZENZEE project.
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# BASE_DIR points to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file if present
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-railway-production-fallback-key-zenzee'


DEBUG = os.getenv('DEBUG', 'True').strip().lower() in ('1', 'true', 'yes', 'on')

# ALLOWED_HOSTS for Railway & Local
raw_allowed_hosts = os.getenv('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = [host.strip() for host in raw_allowed_hosts.split(',') if host.strip()]
if '*' in ALLOWED_HOSTS or os.getenv('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

raw_csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1,http://localhost,https://*.railway.app,https://*.up.railway.app')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in raw_csrf_origins.split(',') if origin.strip()]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local ZENZEE Apps
    'accounts',
    'products',
    'cart',
    'wishlist',
    'orders',
    'reviews',
    'ai',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'backend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'backend' / 'db.sqlite3',
    }
}

# Production DATABASE_URL (Railway PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES['default'] = dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=False
        )
    except Exception:
        from urllib.parse import urlparse
        url = urlparse(DATABASE_URL)
        if url.scheme.startswith('postgres'):
            DATABASES['default'] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': url.path[1:] if url.path else '',
                'USER': url.username or '',
                'PASSWORD': url.password or '',
                'HOST': url.hostname or '',
                'PORT': url.port or 5432,
                'CONN_MAX_AGE': 600,
            }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'backend' / 'media'

# Additional Static Files
STATICFILES_DIRS = [
    BASE_DIR / 'backend' / 'static',
]
STATIC_ROOT = BASE_DIR / 'backend' / 'staticfiles'

# Production Security Settings (enabled when DEBUG=False)
# Note: Railway terminates SSL at its edge proxy. Disabling container-level SSL redirect
# ensures internal HTTP healthchecks (/health/) pass with 200 OK instead of 301 redirects.
if not DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'


# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
