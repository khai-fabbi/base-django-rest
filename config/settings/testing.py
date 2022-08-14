import os

from config.settings.default import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = INSTALLED_APPS + ['drf_yasg']

MIDDLEWARE = MIDDLEWARE + ['helpers.middlewares.QueryCountDebugMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'for_testing',
    }
}

LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')
LOG_FILE_PATH = os.path.join(LOG_DIRECTORY_PATH, 'unittest.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'log_format': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {levelname} {message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'log_format',
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            # 'formatter': 'ltsv',
            'filename': LOG_FILE_PATH,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': LOG_LEVEL,
        'propagate': True,
    },
}
