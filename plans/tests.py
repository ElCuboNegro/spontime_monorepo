from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Plan, InterestTag


class PlanModelTest(TestCase):
    """Tests for Plan model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            handle='test_handle'
        )
        self.now = timezone.now()
        
    def test_plan_creation(self):
        """Test creating a plan."""
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test description',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Test Location',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
            creator=self.user
        )
        self.assertEqual(plan.title, 'Test Plan')
        self.assertTrue(plan.is_active)
        
    def test_is_happening_soon(self):
        """Test is_happening_soon method."""
        plan = Plan.objects.create(
            title='Soon Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Test',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
            creator=self.user
        )
        self.assertTrue(plan.is_happening_soon())
        
        plan2 = Plan.objects.create(
            title='Later Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Test',
            start_time=self.now + timedelta(hours=3),
            end_time=self.now + timedelta(hours=4),
            creator=self.user
        )
        self.assertFalse(plan2.is_happening_soon())
    
    def test_distance_to(self):
        """Test distance calculation."""
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Times Square',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
            creator=self.user
        )
        # Distance to approximately same location
        distance = plan.distance_to(40.7580, -73.9855)
        self.assertLess(distance, 0.1)  # Should be very close
        
        # Distance to Central Park (about 2.5 km away)
        distance = plan.distance_to(40.7829, -73.9654)
        self.assertGreater(distance, 2)
        self.assertLess(distance, 4)


class PlansAPITest(APITestCase):
    """Tests for Plans API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123',
            handle='user_one',
            latitude=40.7580,
            longitude=-73.9855
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            handle='user_two',
            latitude=40.7489,
            longitude=-73.9680
        )
        
        self.tag1 = InterestTag.objects.create(name='Coffee', slug='coffee')
        self.tag2 = InterestTag.objects.create(name='Sports', slug='sports')
        
        self.now = timezone.now()
        
    def test_create_plan(self):
        """Test creating a plan via API."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Coffee Meetup',
            'description': 'Quick coffee',
            'latitude': 40.7580,
            'longitude': -73.9855,
            'location_name': 'Starbucks',
            'start_time': (self.now + timedelta(hours=1)).isoformat(),
            'end_time': (self.now + timedelta(hours=2)).isoformat(),
        }
        response = self.client.post('/api/plans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Coffee Meetup')
        
    def test_now_endpoint_requires_location(self):
        """Test /api/plans/now endpoint requires lat/lon."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/plans/now/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_now_endpoint_with_location(self):
        """Test /api/plans/now endpoint with location parameters."""
        # Create some plans
        plan1 = Plan.objects.create(
            title='Nearby Plan',
            description='Close by',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Times Square',
            start_time=self.now + timedelta(minutes=30),
            end_time=self.now + timedelta(hours=1, minutes=30),
            creator=self.user1
        )
        
        plan2 = Plan.objects.create(
            title='Far Plan',
            description='Far away',
            latitude=40.8580,
            longitude=-73.9855,
            location_name='Far Location',
            start_time=self.now + timedelta(minutes=30),
            end_time=self.now + timedelta(hours=1, minutes=30),
            creator=self.user2
        )
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/plans/now/', {
            'lat': 40.7580,
            'lon': -73.9855,
            'radius': 2
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return nearby plan
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Nearby Plan')
        
    def test_now_endpoint_with_tag_filter(self):
        """Test /api/plans/now endpoint with tag filtering."""
        plan1 = Plan.objects.create(
            title='Coffee Plan',
            description='Coffee',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Cafe',
            start_time=self.now + timedelta(minutes=30),
            end_time=self.now + timedelta(hours=1, minutes=30),
            creator=self.user1
        )
        plan1.tags.add(self.tag1)
        
        plan2 = Plan.objects.create(
            title='Sports Plan',
            description='Basketball',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Court',
            start_time=self.now + timedelta(minutes=30),
            end_time=self.now + timedelta(hours=1, minutes=30),
            creator=self.user2
        )
        plan2.tags.add(self.tag2)
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/plans/now/', {
            'lat': 40.7580,
            'lon': -73.9855,
            'tags': str(self.tag1.id)
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Coffee Plan')
        
    def test_join_plan(self):
        """Test joining a plan."""
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Location',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
            creator=self.user1
        )
        
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/plans/{plan.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(plan.is_member(self.user2))
        
    def test_leave_plan(self):
        """Test leaving a plan."""
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Location',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
            creator=self.user1
        )
        plan.members.add(self.user2)
        
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/plans/{plan.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(plan.is_member(self.user2))

