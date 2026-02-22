from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import Booking
from payments.models import Payment


@shared_task
def cancel_expired_booking(booking_id):
    """
    Cancel a booking if it's still pending after 5 minutes
    This task is scheduled to run 5 minutes after booking creation
    """
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        
        # Only cancel if still pending
        if booking.status == 'pending':
            with transaction.atomic():
                # Update booking status
                booking.status = 'cancelled'
                booking.save()
                
                # Return tickets to event
                event = booking.event
                event.available_tickets += booking.quantity
                event.save()
                
                # Update payment status if exists
                try:
                    payment = Payment.objects.get(booking=booking)
                    payment.status = 'cancelled'
                    payment.save()
                except Payment.DoesNotExist:
                    pass
                
                print(f"[Auto-Cancel] Booking {booking_id} cancelled due to payment timeout")
                return f"Booking {booking_id} cancelled successfully"
        else:
            print(f"[Auto-Cancel] Booking {booking_id} already {booking.status}, skipping cancellation")
            return f"Booking {booking_id} already {booking.status}"
            
    except Booking.DoesNotExist:
        print(f"[Auto-Cancel] Booking {booking_id} not found")
        return f"Booking {booking_id} not found"
    except Exception as e:
        print(f"[Auto-Cancel] Error cancelling booking {booking_id}: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def cleanup_expired_bookings():
    """
    Periodic task to clean up any expired bookings that weren't cancelled
    Run this every 5-10 minutes as a safety net
    """
    expired_bookings = Booking.objects.filter(
        status='pending',
        expires_at__lt=timezone.now()
    )
    
    cancelled_count = 0
    for booking in expired_bookings:
        try:
            with transaction.atomic():
                booking.status = 'cancelled'
                booking.save()
                
                # Return tickets to event
                event = booking.event
                event.available_tickets += booking.quantity
                event.save()
                
                # Update payment status if exists
                try:
                    payment = Payment.objects.get(booking=booking)
                    payment.status = 'cancelled'
                    payment.save()
                except Payment.DoesNotExist:
                    pass
                
                cancelled_count += 1
                print(f"[Cleanup] Cancelled expired booking {booking.booking_id}")
                
        except Exception as e:
            print(f"[Cleanup] Error cancelling booking {booking.booking_id}: {str(e)}")
            continue
    
    return f"Cleaned up {cancelled_count} expired bookings"
