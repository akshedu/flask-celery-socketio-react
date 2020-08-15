#!/bin/sh
set -e

echo "start celery worker"
celery -A tasks worker --loglevel=info -f worker.logs