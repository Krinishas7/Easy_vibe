from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os


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
    
    # Event Details
    venue = models.CharField(max_length=200)
    address = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Ticketing
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Media
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    
    # Status and Timestamps
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
        # Set available_tickets to total_tickets on creation
        if not self.pk:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)
        
        # Resize image if it exists
        if self.image:
            self.resize_image()

    def resize_image(self):
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 600:
            output_size = (600, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def is_available(self):
        return (
            self.status == 'published' and 
            self.available_tickets > 0 and 
            self.start_date > timezone.now()
        )

    @property
    def tickets_sold(self):
        return self.total_tickets - self.available_tickets

    @property
    def is_past(self):
        return self.end_date < timezone.now()
