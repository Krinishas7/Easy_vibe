from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking


class Command(BaseCommand):
    help = 'Clean up expired pending bookings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Hours after which pending bookings expire (default: 24)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']
        
        # Find expired pending bookings
        cutoff_time = timezone.now() - timedelta(hours=hours)
        expired_bookings = Booking.objects.filter(
            status='pending',
            created_at__lt=cutoff_time
        )
        
        count = expired_bookings.count()
        
        if dry_run:
            self.stdout.write(f'Would delete {count} expired bookings')
            for booking in expired_bookings:
                self.stdout.write(f'  - {booking.booking_id} ({booking.event.title})')
        else:
            # Release tickets back to events
            for booking in expired_bookings:
                event = booking.event
                event.available_tickets += booking.quantity
                event.save()
                
                self.stdout.write(f'Released {booking.quantity} tickets for {event.title}')
            
            # Delete expired bookings
            expired_bookings.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cleaned up {count} expired bookings')
            )
