from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from plans.models import Plan
from .models import Message


class MessageAPITest(APITestCase):
    """Tests for Message API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123',
            handle='user_one'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            handle='user_two'
        )
        
        now = timezone.now()
        self.plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Test Location',
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=2),
            creator=self.user1
        )
        self.plan.members.add(self.user2)
        
    def test_member_can_post_message(self):
        """Test that plan members can post messages."""
        self.client.force_authenticate(user=self.user2)
        data = {'content': 'Hello everyone!'}
        response = self.client.post(
            f'/api/plans/{self.plan.id}/messages/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Hello everyone!')
        
    def test_non_member_cannot_post_message(self):
        """Test that non-members cannot post messages."""
        non_member = User.objects.create_user(
            username='outsider',
            password='pass123'
        )
        self.client.force_authenticate(user=non_member)
        data = {'content': 'I want to join!'}
        response = self.client.post(
            f'/api/plans/{self.plan.id}/messages/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_creator_can_post_message(self):
        """Test that plan creator can post messages."""
        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Welcome to my plan!'}
        response = self.client.post(
            f'/api/plans/{self.plan.id}/messages/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_members_can_view_messages(self):
        """Test that members can view messages."""
        Message.objects.create(
            plan=self.plan,
            user=self.user1,
            content='Test message'
        )
        
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/plans/{self.plan.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response has results key (paginated) or is a list
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)
        
    def test_non_members_cannot_view_messages(self):
        """Test that non-members cannot view messages."""
        Message.objects.create(
            plan=self.plan,
            user=self.user1,
            content='Secret message'
        )
        
        non_member = User.objects.create_user(
            username='outsider',
            password='pass123'
        )
        self.client.force_authenticate(user=non_member)
        response = self.client.get(f'/api/plans/{self.plan.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_unauthenticated_cannot_access_messages(self):
        """Test that unauthenticated users cannot access messages."""
        response = self.client.get(f'/api/plans/{self.plan.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MessageModelTest(TestCase):
    """Tests for Message model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            handle='test_handle'
        )
        now = timezone.now()
        self.plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            latitude=40.7580,
            longitude=-73.9855,
            location_name='Test Location',
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=2),
            creator=self.user
        )
        
    def test_message_creation(self):
        """Test creating a message."""
        message = Message.objects.create(
            plan=self.plan,
            user=self.user,
            content='Test message content'
        )
        self.assertEqual(message.content, 'Test message content')
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.plan, self.plan)

