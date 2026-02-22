from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from django.utils import timezone
import uuid


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    # Booking Details
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    
    # Ticket Information
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Contact Information
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Payment Reference
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.event.title}"

    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.event.price * self.quantity
        if not self.expires_at and self.status == 'pending':
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    @property
    def can_be_cancelled(self):
        # Can cancel if booking is confirmed and event hasn't started
        return (
            self.status == 'confirmed' and 
            self.event.start_date > timezone.now()
        )
    
    @property
    def is_expired(self):
        """Check if pending booking has expired"""
        if self.status == 'pending' and self.expires_at:
            return timezone.now() > self.expires_at
        return False


class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField(blank=True)
    
    # QR Code for verification
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # Verification
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.booking.event.title}"

    @property
    def is_valid(self):
        return (
            self.booking.status == 'confirmed' and 
            not self.is_used and 
            self.booking.event.start_date > timezone.now()
        )
