#!/bin/bash

PROJECT_NAME="event_booking"
DJANGO_SETTINGS_MODULE="event_booking.settings"
CELERY_APP="event_booking"

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$(pwd)

echo "Starting Redis..."
redis-server --daemonize yes

sleep 2

echo "Starting Celery worker..."
celery -A $CELERY_APP worker -l info --detach

echo "Starting Celery beat..."
celery -A $CELERY_APP beat -l info --detach

echo "Celery worker and beat started successfully."
