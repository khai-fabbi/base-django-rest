#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ENV_LIST = ('default', 'develop', 'testing', 'production')

ENV_PATH = Path(__file__).resolve().parent / '.env'
load_dotenv(ENV_PATH, override=True)


def main():
    """Run administrative tasks."""

    if 'test' in sys.argv:
        environment = 'testing'
    else:
        environment = os.environ.get('ENV', '').lower()

        if environment not in ENV_LIST:
            raise Exception(f'Setting `ENV` is invalid or missing: `{environment}`')

    settings_module = 'config.settings.' + environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
