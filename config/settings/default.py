"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
import mimetypes

mimetypes.add_type("text/css", ".css", True)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET")

ENV = os.environ.get("ENV", "").lower()

if ENV != "production" and SECRET_KEY is None:
    SECRET_KEY = "ii9f^k10h45_z6cbkxvz^w*uvh0a&f5^j-)0cj^xbgtnlzn*0("

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = int(os.environ.get("DEBUG", 0))
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "apps.authen",
    "apps.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "helpers.middlewares.HandleExceptionMiddleware",
    "helpers.middlewares.PreProcessingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DATABASE_NAME", "fabbi"),
        "USER": os.environ.get("DATABASE_USER", "fabbi"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "123qweA@#"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
        "ATOMIC_REQUESTS": True,
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

SUPPORTED_LANGUAGES = ("en-us", "ja", "vi")

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]


# STATIC_ROOT = '/vol/web/static'

STATIC_ROOT = "static"
STATIC_URL = "/static/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# API
API_ENTRY_POINT = "api/v1/"

# Auth
AUTH_USER_MODEL = "authen.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    # Custom settings.
    "TOKEN_ENDPOINT": "auth/token/",
    "ACCESS_TOKEN_COOKIE": "access_token",
    "REFRESH_TOKEN_COOKIE": "refresh_token",
    "COOKIE_DOMAIN": None,
    "COOKIE_SECURE": False,
    "COOKIE_HTTP_ONLY": True,
    "COOKIE_SAMESITE": "Lax",  # 'Lax', 'Strict', or None
}

# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "libs.rest_framework_simplejwt.authentication.CustomJWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "libs.rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        "drf_excel.renderers.XLSXRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        # 'rest_framework.throttling.AnonRateThrottle',
        # 'rest_framework.throttling.UserRateThrottle'
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "10000/day", "user": "100000/day"},
    "DEFAULT_PAGINATION_CLASS": "libs.rest_framework.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
    "EXCEPTION_HANDLER": "libs.rest_framework.exc_handler.custom_exception_handler",
    "ORDERING_PARAM": "order_by",
}

# Logging
LOG_DIRECTORY_PATH = os.environ.get("LOG_DIRECTORY_PATH", BASE_DIR / "logs")

if not os.path.exists(LOG_DIRECTORY_PATH):
    os.makedirs(LOG_DIRECTORY_PATH)

LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.path.join(LOG_DIRECTORY_PATH, LOG_LEVEL.lower() + ".log")

LOG_FILE_BACKUP = 5
LOG_FILE_SIZE = 1024 * 1024 * 10  # 10Mb

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "log_format": {
            "()": "django.utils.log.ServerFormatter",
            "format": "{server_time} {levelname} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "log_format",
        },
        "file_by_size": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "encoding": "UTF-8",
            "formatter": "log_format",
            "filename": LOG_FILE_PATH,
            "backupCount": LOG_FILE_BACKUP,
            "delay": True,
            "maxBytes": LOG_FILE_SIZE,
        },
        "file_by_time": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "encoding": "UTF-8",
            "formatter": "log_format",
            "filename": LOG_FILE_PATH,
            "backupCount": LOG_FILE_BACKUP,
            "delay": True,
            "interval": 1,
            "utc": True,
            "when": "D",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": [],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file_by_time", "console"],
        "level": LOG_LEVEL,
        "propagate": True,
    },
}
