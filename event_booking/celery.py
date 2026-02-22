import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')

# Initialize Celery app
app = Celery('event_booking')

# Load configuration from Django settings using CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all Django apps
app.autodiscover_tasks()

# Configure periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'cleanup-expired-bookings-every-5-minutes': {
        'task': 'bookings.tasks.cleanup_expired_bookings',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    },
}   
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
