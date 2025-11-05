"""
Management command to generate sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan, CheckIn


class Command(BaseCommand):
    help = 'Generate sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i}',
                    'bio': f'Sample user {i}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                users.append(user)
                self.stdout.write(f'  Created user: {user.username}')
        
        # Create places in NYC area
        places_data = [
            {'name': 'Central Park', 'category': 'park', 'lon': -73.965355, 'lat': 40.782865},
            {'name': 'Empire State Building', 'category': 'landmark', 'lon': -73.985656, 'lat': 40.748817},
            {'name': "Joe's Pizza", 'category': 'restaurant', 'lon': -73.998830, 'lat': 40.730610},
            {'name': 'Brooklyn Bridge', 'category': 'landmark', 'lon': -73.996628, 'lat': 40.706086},
            {'name': 'Times Square', 'category': 'landmark', 'lon': -73.985130, 'lat': 40.758896},
            {'name': 'Prospect Park', 'category': 'park', 'lon': -73.969143, 'lat': 40.660204},
            {'name': 'Starbucks Reserve', 'category': 'cafe', 'lon': -73.994949, 'lat': 40.741895},
            {'name': 'The MET', 'category': 'museum', 'lon': -73.963244, 'lat': 40.779437},
        ]
        
        places = []
        for place_data in places_data:
            place, created = Place.objects.get_or_create(
                name=place_data['name'],
                defaults={
                    'category': place_data['category'],
                    'location': Point(place_data['lon'], place_data['lat'], srid=4326),
                    'address': f'New York, NY',
                    'description': f"Sample {place_data['category']}"
                }
            )
            if created:
                places.append(place)
                self.stdout.write(f'  Created place: {place.name}')
        
        # Create plans
        if users and places:
            for i, place in enumerate(places[:3]):
                plan, created = Plan.objects.get_or_create(
                    title=f'Visit {place.name}',
                    defaults={
                        'description': f'Let\'s visit {place.name} together!',
                        'creator': users[i % len(users)],
                        'place': place,
                        'scheduled_time': timezone.now() + timedelta(days=i+1),
                        'status': 'active'
                    }
                )
                if created:
                    # Add participants
                    plan.participants.add(*users[:2])
                    self.stdout.write(f'  Created plan: {plan.title}')
        
        # Create check-ins
        if users and places:
            for i, user in enumerate(users):
                for place in places[i:i+3]:
                    checkin, created = CheckIn.objects.get_or_create(
                        user=user,
                        place=place,
                        defaults={'notes': f'Great place!'}
                    )
                    if created:
                        self.stdout.write(f'  Created check-in: {user.username} @ {place.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
