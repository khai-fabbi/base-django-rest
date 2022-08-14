import random

from django.core.management.base import BaseCommand

AVAILABLE_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


class Command(BaseCommand):
    help = 'Command for generating secret key.'

    def handle(self, *args, **options):
        # Generate new Django secret key.
        generated_secret_key = ''.join([random.choice(AVAILABLE_CHARACTERS) for i in range(50)])

        # Output to terminal
        self.stdout.write(self.style.SUCCESS('New generated secret key: %s' % generated_secret_key))
