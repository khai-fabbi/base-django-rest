from config.settings.default import *

ALLOWED_HOSTS = ['*']

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

INSTALLED_APPS = INSTALLED_APPS + ['drf_yasg']

MIDDLEWARE = MIDDLEWARE + ['helpers.middlewares.QueryCountDebugMiddleware']
