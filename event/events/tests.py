from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Event, Category


class EventModelTest(TestCase):
    def setUp(self):
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

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Test Concert")
        self.assertEqual(self.event.category, self.category)
        self.assertEqual(self.event.available_tickets, 100)

    def test_event_str_method(self):
        self.assertEqual(str(self.event), "Test Concert")

    def test_is_available_method(self):
        self.assertTrue(self.event.is_available())
        
        # Make event sold out
        self.event.available_tickets = 0
        self.event.save()
        self.assertFalse(self.event.is_available())

    def test_is_past_event(self):
        # Future event
        self.assertFalse(self.event.is_past_event())
        
        # Past event
        self.event.date = timezone.now() - timedelta(days=1)
        self.event.save()
        self.assertTrue(self.event.is_past_event())


class EventViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_home_view(self):
        response = self.client.get(reverse('events:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Concert")

    def test_event_list_view(self):
        response = self.client.get(reverse('events:event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Concert")

    def test_event_detail_view(self):
        response = self.client.get(reverse('events:event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Concert")
        self.assertContains(response, "Test Venue")
