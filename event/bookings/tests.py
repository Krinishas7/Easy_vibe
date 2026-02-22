from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Category
from .models import Booking, Ticket


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Music",
            description="Music events"
        )
        self.event = Event.objects.create(
            title="Test Concert",
            description="A test concert event",
            date=timezone.now() + timedelta(days=30),
            venue="Test Venue",
            address="Test Address",
            price=1000.00,
            total_tickets=100,
            available_tickets=100,
            category=self.category,
            status='published'
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            quantity=2,
            total_amount=2000.00,
            contact_name="Test User",
            contact_email="test@example.com",
            contact_phone="1234567890"
        )
        self.assertEqual(booking.quantity, 2)
        self.assertEqual(booking.total_amount, 2000.00)
        self.assertEqual(booking.status, 'pending')

    def test_ticket_generation(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            quantity=2,
            total_amount=2000.00,
            contact_name="Test User",
            contact_email="test@example.com",
            contact_phone="1234567890"
        )
        
        # Generate tickets
        for i in range(booking.quantity):
            Ticket.objects.create(
                booking=booking,
                ticket_number=f"TKT-{booking.booking_id}-{i+1:03d}"
            )
        
        self.assertEqual(booking.tickets.count(), 2)


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Music",
            description="Music events"
        )
        self.event = Event.objects.create(
            title="Test Concert",
            description="A test concert event",
            date=timezone.now() + timedelta(days=30),
            venue="Test Venue",
            address="Test Address",
            price=1000.00,
            total_tickets=100,
            available_tickets=100,
            category=self.category,
            status='published'
        )

    def test_my_bookings_requires_login(self):
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_my_bookings_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 200)
