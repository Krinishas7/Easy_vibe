#!/usr/bin/env python
"""
Test email sending functionality
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from bookings.models import Booking
from bookings.utils import send_booking_confirmation_email

def test_email_sending():
    """Test sending booking confirmation email"""
    try:
        # Get a confirmed booking
        booking = Booking.objects.filter(status='confirmed').first()
        
        if not booking:
            print("No confirmed bookings found. Creating a test scenario...")
            return
        
        print(f"Sending test email for booking: {booking.booking_id}")
        
        # Send email
        success = send_booking_confirmation_email(booking)
        
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    test_email_sending()
