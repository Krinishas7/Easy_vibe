from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')

    venue = models.CharField(max_length=200)
    address = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # -----------------------------
    # COUNTRY-BASED BOOKING CONTROL (ADMIN)
    # -----------------------------
    country = models.CharField(max_length=100, default="Nepal")
    allow_any_country = models.BooleanField(default=True)
    # -----------------------------

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 600:
                img.thumbnail((600, 400))
                img.save(self.image.path)

    @property
    def is_available(self):
        return (
            self.status == 'published'
            and self.available_tickets > 0
            and self.start_date > timezone.now()
        )

    @property
    def tickets_sold(self):
        return self.total_tickets - self.available_tickets

    @property
    def is_past(self):
        return self.end_date < timezone.now()

    def update_event_ticket_counts(self):
        total = sum(s.total_seats for s in self.seat_types.all())
        available = sum(s.seats_available for s in self.seat_types.all())

        self.total_tickets = total
        self.available_tickets = available
        self.save(update_fields=["total_tickets", "available_tickets"])


class SeatType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='seat_types')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    total_seats = models.PositiveIntegerField(default=0)
    seats_available = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('event', 'name')
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    @property
    def tickets_sold(self):
        return self.bookings.filter(status="confirmed").count()

    @property
    def seat_overflow(self):
        return max(self.tickets_sold - self.total_seats, 0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self.seats_available = self.total_seats

        super().save(*args, **kwargs)

        sold = self.bookings.filter(status="confirmed").count()
        self.seats_available = max(self.total_seats - sold, 0)
        super().save(update_fields=["seats_available"])

        self.event.update_event_ticket_counts()
