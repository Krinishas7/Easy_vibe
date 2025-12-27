from django.db import models
from bookings.models import Booking
from django.utils import timezone


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='esewa')
    
    # eSewa specific fields
    esewa_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    esewa_reference_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.booking.booking_id}"

    def mark_completed(self, transaction_id=None, reference_id=None):
        self.status = 'completed'
        self.completed_at = timezone.now()
        if transaction_id:
            self.esewa_transaction_id = transaction_id
        if reference_id:
            self.esewa_reference_id = reference_id
        self.save()
        
        # Update booking status
        self.booking.status = 'confirmed'
        self.booking.save()

    def mark_failed(self):
        self.status = 'failed'
        self.save()
        
        # Update booking status
        self.booking.status = 'cancelled'
        self.booking.save()
