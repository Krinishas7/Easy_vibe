#!/usr/bin/env python
"""
Database setup script for Event Booking System
Run this script to create the database tables and initial data
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from events.models import Category, Event
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify

def create_database():
    """Create database tables"""
    print("Creating database tables...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("Database tables created successfully!")

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            username='admin',
            email='admin@eventbook.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("Superuser created: username=admin, password=admin123")
    else:
        print("Superuser already exists")

def create_sample_data():
    """Create sample categories and events"""
    print("Creating sample data...")
    
    # Create categories
    categories_data = [
        {'name': 'Music & Concerts', 'description': 'Live music performances and concerts'},
        {'name': 'Technology', 'description': 'Tech conferences, workshops, and seminars'},
        {'name': 'Sports', 'description': 'Sporting events and competitions'},
        {'name': 'Arts & Culture', 'description': 'Art exhibitions, cultural events, and performances'},
        {'name': 'Business', 'description': 'Business conferences, networking events, and workshops'},
        {'name': 'Food & Drink', 'description': 'Food festivals, wine tastings, and culinary events'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Get admin user for events
    admin_user = User.objects.get(username='admin')
    
    events_data = [
        {
            'title': 'Rock Music Festival 2025',
            'description': 'Join us for an electrifying rock music festival featuring top international and local bands. Experience three days of non-stop music, food, and entertainment under the stars!',
            'category': 'Music & Concerts',
            'venue': 'City Stadium',
            'address': 'Downtown, Kathmandu',
            'price': 2500.00,
            'total_tickets': 1000,
            'days_ahead': 45,  # 45 days from now
        },
        {
            'title': 'Tech Conference Nepal 2025',
            'description': 'Annual technology conference featuring the latest trends in AI, blockchain, cloud computing, and web development. Network with industry leaders and learn from expert speakers.',
            'category': 'Technology',
            'venue': 'Hotel Yak & Yeti',
            'address': 'Durbar Marg, Kathmandu',
            'price': 5000.00,
            'total_tickets': 500,
            'days_ahead': 30,
        },
        {
            'title': 'Football Championship Finals',
            'description': 'Watch the most exciting football championship finals with teams from across the valley competing for the ultimate trophy. Bring your family and friends for an unforgettable experience!',
            'category': 'Sports',
            'venue': 'Dasharath Stadium',
            'address': 'Tripureshwor, Kathmandu',
            'price': 500.00,
            'total_tickets': 2000,
            'days_ahead': 20,
        },
        {
            'title': 'Contemporary Art Exhibition 2025',
            'description': 'Explore stunning contemporary art from local and international artists. This exhibition showcases paintings, sculptures, and digital art that push creative boundaries.',
            'category': 'Arts & Culture',
            'venue': 'Nepal Art Council',
            'address': 'Babar Mahal, Kathmandu',
            'price': 300.00,
            'total_tickets': 200,
            'days_ahead': 15,
        },
        {
            'title': 'Startup Summit 2025',
            'description': 'Connect with entrepreneurs, investors, and innovators at Nepal\'s premier startup event. Pitch competitions, workshops, and networking sessions included.',
            'category': 'Business',
            'venue': 'Soaltee Hotel',
            'address': 'Tahachal, Kathmandu',
            'price': 3500.00,
            'total_tickets': 300,
            'days_ahead': 60,
        },
        {
            'title': 'Food & Wine Festival',
            'description': 'Indulge in a culinary journey featuring the finest cuisines and wines from around the world. Celebrity chefs, cooking demonstrations, and tastings await!',
            'category': 'Food & Drink',
            'venue': 'Hyatt Regency',
            'address': 'Boudha, Kathmandu',
            'price': 1500.00,
            'total_tickets': 400,
            'days_ahead': 25,
        },
        {
            'title': 'Jazz Night Under the Stars',
            'description': 'An intimate evening of smooth jazz performed by renowned musicians. Enjoy great music, drinks, and ambiance in a beautiful outdoor setting.',
            'category': 'Music & Concerts',
            'venue': 'Garden of Dreams',
            'address': 'Thamel, Kathmandu',
            'price': 1200.00,
            'total_tickets': 150,
            'days_ahead': 10,
        },
        {
            'title': 'Marathon for Charity',
            'description': 'Run for a cause! Join thousands of runners in this annual charity marathon. All proceeds go to local education and healthcare initiatives.',
            'category': 'Sports',
            'venue': 'Tundikhel Ground',
            'address': 'Kathmandu Durbar Square Area',
            'price': 800.00,
            'total_tickets': 1500,
            'days_ahead': 35,
        },
    ]
    
    for event_data in events_data:
        category = Category.objects.get(name=event_data['category'])
        
        if not Event.objects.filter(title=event_data['title']).exists():
            start_date = timezone.now() + timedelta(days=event_data['days_ahead'])
            end_date = start_date + timedelta(hours=8)  # 8 hour events
            
            event = Event.objects.create(
                title=event_data['title'],
                slug=slugify(event_data['title']),
                description=event_data['description'],
                category=category,
                organizer=admin_user,
                venue=event_data['venue'],
                address=event_data['address'],
                start_date=start_date,
                end_date=end_date,
                total_tickets=event_data['total_tickets'],
                price=event_data['price'],
                status='published'
            )
            print(f"Created event: {event.title} (starts in {event_data['days_ahead']} days)")
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    print("=" * 60)
    print("Setting up Event Booking System Database...")
    print("=" * 60)
    create_database()
    create_superuser()
    create_sample_data()
    print("\n" + "=" * 60)
    print("Database setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000/")
    print("3. Admin panel: http://localhost:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 60)
