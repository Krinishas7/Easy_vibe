import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv

# ===========================
# LOAD ENVIRONMENT VARIABLES
# ===========================
load_dotenv()  # Load .env if exists

# ===========================
# PATH SETTINGS
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# SECURITY SETTINGS
# ===========================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

# ⚠️ Development: keep True to serve static files and allow debugging
DEBUG = config('DEBUG', default=False, cast=bool)

# Allow localhost and any IP during development
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# ===========================
# APPLICATIONS
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'bookings',
    'payments',
    'accounts',
    'django_celery_beat',
    'django_celery_results',
]
INSTALLED_APPS += ['sslserver']

# ===========================
# MIDDLEWARE
# ===========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_booking.urls'
CSRF_TRUSTED_ORIGINS = [
    "https://765f395ec7c1.ngrok-free.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://08ec449b02b9.ngrok-free.app",
]



# ===========================
# TEMPLATES
# ===========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'event_booking.wsgi.application'

# ===========================
# DATABASE
# ===========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================
# PASSWORD VALIDATION
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===========================
# INTERNATIONALIZATION
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ===========================
# STATIC AND MEDIA FILES
# ===========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Local static files
STATIC_ROOT = BASE_DIR / 'staticfiles'    # collectstatic destination

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================
# DEFAULT PRIMARY KEY
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================
# LOGIN SETTINGS
# ===========================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ===========================
# ESEWA CONFIGURATION
# ===========================
ESEWA_MERCHANT_ID = config('ESEWA_MERCHANT_ID', default='EPAYTEST')
ESEWA_SECRET_KEY = config('ESEWA_SECRET_KEY', default='8gBm/:&EnhH.1/q')
ESEWA_SUCCESS_URL = config('ESEWA_SUCCESS_URL', default='http://localhost:8000/payments/success/')
ESEWA_FAILURE_URL = config('ESEWA_FAILURE_URL', default='http://localhost:8000/payments/failure/')

# ===========================
# EMAIL CONFIGURATION
# ===========================
# ===========================
# EMAIL CONFIGURATION
# ===========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='ashimbashyal13@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='psqjuotsicjoevul')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='EventVibe <ashimbashyal13@gmail.com>')

# ===========================
# DEBUG EMAIL BACKEND
# ===========================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("[DEBUG MODE] Emails will be printed to the console instead of being sent.")

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kathmandu'  # Or your timezone
