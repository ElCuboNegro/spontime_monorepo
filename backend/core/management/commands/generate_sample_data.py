"""
Management command to generate sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan, CheckIn, Attendance


class Command(BaseCommand):
    help = 'Generate sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                handle=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'display_name': f'User {i}',
                    'language': 'en',
                    'status': 'active'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                users.append(user)
                self.stdout.write(f'  Created user: {user.handle}')
        
        # Create places in NYC area
        places_data = [
            {'name': 'Central Park', 'lon': -73.965355, 'lat': 40.782865},
            {'name': 'Empire State Building', 'lon': -73.985656, 'lat': 40.748817},
            {'name': "Joe's Pizza", 'lon': -73.998830, 'lat': 40.730610},
            {'name': 'Brooklyn Bridge', 'lon': -73.996628, 'lat': 40.706086},
            {'name': 'Times Square', 'lon': -73.985130, 'lat': 40.758896},
            {'name': 'Prospect Park', 'lon': -73.969143, 'lat': 40.660204},
            {'name': 'Starbucks Reserve', 'lon': -73.994949, 'lat': 40.741895},
            {'name': 'The MET', 'lon': -73.963244, 'lat': 40.779437},
        ]
        
        places = []
        for place_data in places_data:
            place, created = Place.objects.get_or_create(
                name=place_data['name'],
                defaults={
                    'location': Point(place_data['lon'], place_data['lat'], srid=4326),
                    'address': f'New York, NY',
                    'city': 'New York',
                    'country': 'USA',
                    'tags': []
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
                        'host_user': users[i % len(users)],
                        'place': place,
                        'starts_at': timezone.now() + timedelta(days=i+1),
                        'ends_at': timezone.now() + timedelta(days=i+1, hours=2),
                        'visibility': 'public',
                        'is_active': True,
                        'tags': []
                    }
                )
                if created:
                    # Add attendances
                    for user in users[:2]:
                        Attendance.objects.get_or_create(
                            plan=plan,
                            user=user,
                            defaults={'status': 'joined'}
                        )
                    self.stdout.write(f'  Created plan: {plan.title}')
        
        # Create check-ins
        if users and places:
            for i, user in enumerate(users):
                for place in places[i:i+3]:
                    # Create a plan for the check-in
                    past_plan, _ = Plan.objects.get_or_create(
                        title=f'{user.handle} at {place.name}',
                        defaults={
                            'host_user': user,
                            'place': place,
                            'starts_at': timezone.now() - timedelta(days=i+1),
                            'ends_at': timezone.now() - timedelta(days=i+1, hours=-2),
                            'is_active': False
                        }
                    )
                    
                    checkin, created = CheckIn.objects.get_or_create(
                        user=user,
                        plan=past_plan,
                        defaults={'geo': place.location}
                    )
                    if created:
                        self.stdout.write(f'  Created check-in: {user.handle} @ {place.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
