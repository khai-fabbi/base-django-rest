"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

ENV_LIST = ('default', 'develop', 'testing', 'production')

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(ENV_PATH, override=True)

if 'test' in sys.argv:
    environment = 'testing'
else:
    environment = os.environ.get('ENV', '').lower()

    if environment not in ENV_LIST:
        raise Exception(f'Setting `ENV` is invalid or missing: `{environment}`')

settings_module = 'config.settings.' + environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
