from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User
from plans.models import Plan, InterestTag
from chat.models import Message


class Command(BaseCommand):
    help = 'Seed the database with sample data for Spontime'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create interest tags
        tags_data = [
            ('Coffee', 'coffee'),
            ('Sports', 'sports'),
            ('Food', 'food'),
            ('Music', 'music'),
            ('Art', 'art'),
            ('Study', 'study'),
            ('Gaming', 'gaming'),
            ('Hiking', 'hiking'),
        ]
        
        tags = {}
        for name, slug in tags_data:
            tag, created = InterestTag.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            tags[slug] = tag
            if created:
                self.stdout.write(f'Created tag: {name}')
        
        # Create sample users
        users_data = [
            {
                'username': 'alice_smith',
                'email': 'alice@example.com',
                'handle': 'alice_spontime',
                'photo_url': 'https://i.pravatar.cc/150?img=1',
                'bio': 'Love spontaneous adventures!',
                'latitude': 40.7580,
                'longitude': -73.9855,
            },
            {
                'username': 'bob_jones',
                'email': 'bob@example.com',
                'handle': 'bob_active',
                'photo_url': 'https://i.pravatar.cc/150?img=2',
                'bio': 'Always up for coffee or sports',
                'latitude': 40.7489,
                'longitude': -73.9680,
            },
            {
                'username': 'charlie_dev',
                'email': 'charlie@example.com',
                'handle': 'charlie_codes',
                'photo_url': 'https://i.pravatar.cc/150?img=3',
                'bio': 'Tech enthusiast and foodie',
                'latitude': 40.7614,
                'longitude': -73.9776,
            },
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'handle': user_data['handle'],
                    'photo_url': user_data['photo_url'],
                    'bio': user_data['bio'],
                    'latitude': user_data['latitude'],
                    'longitude': user_data['longitude'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)
        
        # Create sample plans
        now = timezone.now()
        plans_data = [
            {
                'title': 'Quick Coffee at Starbucks',
                'description': 'Need a caffeine fix! Anyone want to join?',
                'latitude': 40.7580,
                'longitude': -73.9855,
                'location_name': 'Starbucks, Times Square',
                'start_time': now + timedelta(minutes=30),
                'end_time': now + timedelta(hours=1, minutes=30),
                'creator': users[0],
                'tags': ['coffee'],
                'members': [users[1]],
            },
            {
                'title': 'Pickup Basketball Game',
                'description': 'Looking for 3 more players for a friendly game',
                'latitude': 40.7489,
                'longitude': -73.9680,
                'location_name': 'Bryant Park Basketball Court',
                'start_time': now + timedelta(hours=1),
                'end_time': now + timedelta(hours=3),
                'creator': users[1],
                'tags': ['sports'],
                'members': [users[0], users[2]],
            },
            {
                'title': 'Lunch at Food Trucks',
                'description': 'Checking out the new food trucks on 6th Ave!',
                'latitude': 40.7614,
                'longitude': -73.9776,
                'location_name': '6th Avenue Food Trucks',
                'start_time': now + timedelta(minutes=45),
                'end_time': now + timedelta(hours=1, minutes=45),
                'creator': users[2],
                'tags': ['food'],
                'members': [],
            },
            {
                'title': 'Museum Visit - MoMA',
                'description': 'Spontaneous art appreciation session',
                'latitude': 40.7614,
                'longitude': -73.9776,
                'location_name': 'Museum of Modern Art',
                'start_time': now + timedelta(hours=2),
                'end_time': now + timedelta(hours=4),
                'creator': users[0],
                'tags': ['art'],
                'members': [users[2]],
            },
        ]
        
        created_plans = []
        for plan_data in plans_data:
            tag_slugs = plan_data.pop('tags', [])
            member_users = plan_data.pop('members', [])
            
            plan, created = Plan.objects.get_or_create(
                title=plan_data['title'],
                creator=plan_data['creator'],
                defaults=plan_data
            )
            
            if created:
                # Add tags
                for tag_slug in tag_slugs:
                    if tag_slug in tags:
                        plan.tags.add(tags[tag_slug])
                
                # Add members
                for member in member_users:
                    plan.members.add(member)
                
                self.stdout.write(f'Created plan: {plan.title}')
                created_plans.append(plan)
        
        # Create sample messages
        if created_plans:
            messages_data = [
                {
                    'plan': created_plans[0],
                    'user': users[1],
                    'content': "I'm in! What time exactly?",
                },
                {
                    'plan': created_plans[0],
                    'user': users[0],
                    'content': "Let's meet at 3:30 PM!",
                },
                {
                    'plan': created_plans[1],
                    'user': users[0],
                    'content': "Count me in! Haven't played in a while though",
                },
                {
                    'plan': created_plans[1],
                    'user': users[1],
                    'content': "No worries, it's just for fun!",
                },
                {
                    'plan': created_plans[1],
                    'user': users[2],
                    'content': "I'll bring the basketball",
                },
            ]
            
            for msg_data in messages_data:
                msg, created = Message.objects.get_or_create(
                    plan=msg_data['plan'],
                    user=msg_data['user'],
                    content=msg_data['content'],
                )
                if created:
                    self.stdout.write(f'Created message in plan: {msg.plan.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
