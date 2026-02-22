from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Category
import random


class Command(BaseCommand):
    help = 'Create sample events for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of events to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Create categories if they don't exist
        categories_data = [
            ('Music', 'Concerts, festivals, and musical performances'),
            ('Technology', 'Tech conferences, workshops, and seminars'),
            ('Sports', 'Sporting events and competitions'),
            ('Arts', 'Art exhibitions, theater, and cultural events'),
            ('Business', 'Business conferences and networking events'),
            ('Education', 'Educational workshops and training sessions'),
        ]
        
        categories = []
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # Sample event data
        event_templates = [
            {
                'title': 'Summer Music Festival',
                'description': 'Join us for an amazing summer music festival featuring top artists from around the world.',
                'venue': 'Central Park Amphitheater',
                'address': 'Central Park, Kathmandu',
                'price_range': (500, 2000),
                'ticket_range': (100, 500),
            },
            {
                'title': 'Tech Innovation Summit',
                'description': 'Discover the latest trends in technology and innovation at this premier tech summit.',
                'venue': 'Convention Center',
                'address': 'Bhrikutimandap, Kathmandu',
                'price_range': (1000, 5000),
                'ticket_range': (50, 200),
            },
            {
                'title': 'Art & Culture Exhibition',
                'description': 'Experience the rich cultural heritage through this comprehensive art exhibition.',
                'venue': 'National Art Gallery',
                'address': 'Bhaktapur Durbar Square',
                'price_range': (200, 800),
                'ticket_range': (80, 300),
            },
            {
                'title': 'Business Networking Event',
                'description': 'Connect with industry leaders and expand your professional network.',
                'venue': 'Hotel Yak & Yeti',
                'address': 'Durbar Marg, Kathmandu',
                'price_range': (800, 3000),
                'ticket_range': (30, 150),
            },
            {
                'title': 'Football Championship',
                'description': 'Watch the most exciting football matches of the season.',
                'venue': 'Dasharath Stadium',
                'address': 'Tripureshwor, Kathmandu',
                'price_range': (300, 1500),
                'ticket_range': (200, 1000),
            },
        ]

        created_count = 0
        for i in range(count):
            template = random.choice(event_templates)
            category = random.choice(categories)
            
            # Generate random date between 1 and 90 days from now
            days_ahead = random.randint(1, 90)
            event_date = timezone.now() + timedelta(days=days_ahead)
            
            # Random price and tickets
            price = random.randint(*template['price_range'])
            total_tickets = random.randint(*template['ticket_range'])
            
            # Create unique title
            title = f"{template['title']} {i+1}"
            
            event = Event.objects.create(
                title=title,
                description=template['description'],
                date=event_date,
                venue=template['venue'],
                address=template['address'],
                price=price,
                total_tickets=total_tickets,
                available_tickets=total_tickets,
                category=category,
                status='published'
            )
            
            created_count += 1
            self.stdout.write(f'Created event: {event.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample events')
        )
