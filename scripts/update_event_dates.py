#!/usr/bin/env python
"""
Script to update existing event dates to future dates
Run this if your events are showing as "Not Available"
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from events.models import Event
from django.utils import timezone
from datetime import timedelta

def update_event_dates():
    """Update all events to have future dates"""
    print("Updating event dates to future dates...")
    
    events = Event.objects.all()
    updated_count = 0
    
    for idx, event in enumerate(events, start=1):
        # Set event to start in 10-60 days from now
        days_ahead = 10 + (idx * 5)
        start_date = timezone.now() + timedelta(days=days_ahead)
        end_date = start_date + timedelta(hours=8)
        
        event.start_date = start_date
        event.end_date = end_date
        event.status = 'published'
        event.save()
        
        updated_count += 1
        print(f"✓ Updated: {event.title} - starts in {days_ahead} days")
    
    print(f"\n{updated_count} events updated successfully!")
    print("All events are now available for booking.")

if __name__ == '__main__':
    print("=" * 60)
    print("Event Date Updater")
    print("=" * 60)
    update_event_dates()
    print("=" * 60)
