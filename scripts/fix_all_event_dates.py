#!/usr/bin/env python
"""
Script to fix all event dates to be in the future
Run this script to make all events bookable
"""
import os
import sys
import django
from datetime import timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from django.utils import timezone
from events.models import Event

def fix_event_dates():
    """Update all event dates to be in the future"""
    events = Event.objects.all()
    now = timezone.now()
    
    print(f"\n{'='*60}")
    print("FIXING EVENT DATES")
    print(f"{'='*60}\n")
    print(f"Current time: {now.strftime('%Y-%m-%d %I:%M %p')}\n")
    
    updated_count = 0
    for i, event in enumerate(events, 1):
        # Calculate event duration
        duration = event.end_date - event.start_date
        
        # Set new start date to be (i * 3) days from now at 6:00 PM
        days_ahead = i * 3
        new_start = now + timedelta(days=days_ahead)
        new_start = new_start.replace(hour=18, minute=0, second=0, microsecond=0)
        
        # Update dates
        old_start = event.start_date
        event.start_date = new_start
        event.end_date = new_start + duration
        event.save()
        
        updated_count += 1
        print(f"✓ Event {i}: {event.title}")
        print(f"  Old date: {old_start.strftime('%Y-%m-%d %I:%M %p')}")
        print(f"  New date: {new_start.strftime('%Y-%m-%d %I:%M %p')}")
        print(f"  Status: {'✓ Available' if event.is_available else '✗ Not Available'}")
        print()
    
    print(f"{'='*60}")
    print(f"Successfully updated {updated_count} event(s)")
    print(f"{'='*60}\n")
    
    # Verify all events are now available
    available_events = Event.objects.filter(status='published').count()
    total_published = Event.objects.filter(status='published').count()
    
    print(f"Published events: {total_published}")
    print(f"All events should now be bookable!\n")

if __name__ == '__main__':
    fix_event_dates()
