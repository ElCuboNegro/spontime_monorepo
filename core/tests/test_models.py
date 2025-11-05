"""
Unit tests for Spontime models.
"""
import pytest
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan, CheckIn, Cluster, Recommendation


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""
    
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
    
    def test_user_str(self):
        user = User.objects.create_user(username='testuser', password='test')
        assert str(user) == 'testuser'


@pytest.mark.django_db
class TestPlaceModel:
    """Test Place model."""
    
    def test_place_creation(self):
        place = Place.objects.create(
            name='Test Place',
            description='A test place',
            location=Point(-74.0060, 40.7128, srid=4326),
            address='123 Test St',
            category='restaurant'
        )
        assert place.name == 'Test Place'
        assert place.category == 'restaurant'
        assert place.location.x == -74.0060
        assert place.location.y == 40.7128
    
    def test_place_str(self):
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        assert str(place) == 'Test Place'


@pytest.mark.django_db
class TestPlanModel:
    """Test Plan model."""
    
    def test_plan_creation(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            description='A test plan',
            creator=user,
            place=place,
            scheduled_time=timezone.now() + timedelta(days=1),
            status='active'
        )
        assert plan.title == 'Test Plan'
        assert plan.creator == user
        assert plan.place == place
        assert plan.status == 'active'
    
    def test_plan_str(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            creator=user,
            place=place,
            scheduled_time=timezone.now()
        )
        assert str(plan) == 'Test Plan'


@pytest.mark.django_db
class TestCheckInModel:
    """Test CheckIn model."""
    
    def test_checkin_creation(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        checkin = CheckIn.objects.create(
            user=user,
            place=place,
            notes='Great place!'
        )
        assert checkin.user == user
        assert checkin.place == place
        assert checkin.notes == 'Great place!'
    
    def test_checkin_str(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        checkin = CheckIn.objects.create(user=user, place=place)
        assert str(checkin) == 'testuser @ Test Place'


@pytest.mark.django_db
class TestClusterModel:
    """Test Cluster model."""
    
    def test_cluster_creation(self):
        place1 = Place.objects.create(
            name='Place 1',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        place2 = Place.objects.create(
            name='Place 2',
            location=Point(-74.0070, 40.7130, srid=4326)
        )
        cluster = Cluster.objects.create(
            cluster_id=1,
            centroid=Point(-74.0065, 40.7129, srid=4326),
            radius=100.0
        )
        cluster.places.add(place1, place2)
        
        assert cluster.cluster_id == 1
        assert cluster.places.count() == 2
        assert cluster.radius == 100.0
    
    def test_cluster_str(self):
        cluster = Cluster.objects.create(
            cluster_id=42,
            centroid=Point(-74.0065, 40.7129, srid=4326),
            radius=100.0
        )
        assert str(cluster) == 'Cluster 42'


@pytest.mark.django_db
class TestRecommendationModel:
    """Test Recommendation model."""
    
    def test_recommendation_creation(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Recommended Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        rec = Recommendation.objects.create(
            user=user,
            place=place,
            score=0.85,
            reason='Similar to places you like'
        )
        assert rec.user == user
        assert rec.place == place
        assert rec.score == 0.85
        assert rec.reason == 'Similar to places you like'
    
    def test_recommendation_str(self):
        user = User.objects.create_user(username='testuser', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        rec = Recommendation.objects.create(
            user=user,
            place=place,
            score=0.75
        )
        assert 'Test Place' in str(rec)
        assert 'testuser' in str(rec)
        assert '0.75' in str(rec)
