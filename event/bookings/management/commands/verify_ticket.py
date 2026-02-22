from django.core.management.base import BaseCommand
from bookings.utils import verify_ticket_qr


class Command(BaseCommand):
    help = 'Verify a ticket using QR code data'

    def add_arguments(self, parser):
        parser.add_argument('qr_data', type=str, help='QR code data to verify')

    def handle(self, *args, **options):
        qr_data = options['qr_data']
        
        is_valid, result = verify_ticket_qr(qr_data)
        
        if is_valid:
            ticket_info = result
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Valid Ticket!\n"
                    f"Event: {ticket_info['event'].title}\n"
                    f"Attendee: {ticket_info['ticket'].attendee_name}\n"
                    f"Ticket ID: {ticket_info['ticket'].ticket_id}\n"
                    f"Booking ID: {ticket_info['booking'].booking_id}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ Invalid Ticket: {result}")
            )
