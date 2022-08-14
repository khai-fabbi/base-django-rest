#!/bin/sh

set -e

python manage.py collectstatic --noinput

# uwsgi -l 4096 --processes 8 --threads 2 --socket :8008 --master --vacuum --die-on-term --enable-threads --module config.wsgi --protocol=http --pidfile=/tmp/fabbi.pid --stats /tmp/stats.socket
# uwsgi -l 1024 --processes 2 --threads 2 --http :8008 --stats :8009 --stats-http --master --enable-threads --module config.wsgi --pidfile=/tmp/fabbi.pid

uwsgi --ini /scripts/uwsgi.ini