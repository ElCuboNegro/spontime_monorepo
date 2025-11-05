"""
Unit tests for Spontime models.
"""
import pytest
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan, CheckIn, Cluster, Attendance, Venue, Partner


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""
    
    def test_user_creation(self):
        user = User.objects.create_user(
            handle='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.handle == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
    
    def test_user_str(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        assert str(user) == 'testuser'


@pytest.mark.django_db
class TestPlaceModel:
    """Test Place model."""
    
    def test_place_creation(self):
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326),
            address='123 Test St',
            city='New York',
            country='USA'
        )
        assert place.name == 'Test Place'
        assert place.city == 'New York'
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
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            description='A test plan',
            host_user=user,
            place=place,
            starts_at=timezone.now() + timedelta(days=1),
            ends_at=timezone.now() + timedelta(days=1, hours=2),
            visibility='public',
            is_active=True
        )
        assert plan.title == 'Test Plan'
        assert plan.host_user == user
        assert plan.place == place
        assert plan.is_active is True
    
    def test_plan_str(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            description='Test',
            host_user=user,
            place=place,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(hours=2)
        )
        assert str(plan) == 'Test Plan'


@pytest.mark.django_db
class TestAttendanceModel:
    """Test Attendance model."""
    
    def test_attendance_creation(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            host_user=user,
            place=place,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(hours=2)
        )
        attendance = Attendance.objects.create(
            user=user,
            plan=plan,
            status='joined'
        )
        assert attendance.user == user
        assert attendance.plan == plan
        assert attendance.status == 'joined'


@pytest.mark.django_db
class TestCheckInModel:
    """Test CheckIn model."""
    
    def test_checkin_creation(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        place = Place.objects.create(
            name='Test Place',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        plan = Plan.objects.create(
            title='Test Plan',
            host_user=user,
            place=place,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(hours=2)
        )
        checkin = CheckIn.objects.create(
            user=user,
            plan=plan,
            geo=Point(-74.0060, 40.7128, srid=4326)
        )
        assert checkin.user == user
        assert checkin.plan == plan
        assert checkin.geo is not None


@pytest.mark.django_db
class TestClusterModel:
    """Test Cluster model."""
    
    def test_cluster_creation(self):
        cluster = Cluster.objects.create(
            label='Test Cluster',
            centroid=Point(-74.0065, 40.7129, srid=4326),
            scope='places',
            plan_count=0
        )
        assert cluster.label == 'Test Cluster'
        assert cluster.scope == 'places'
        assert cluster.plan_count == 0
    
    def test_cluster_str(self):
        cluster = Cluster.objects.create(
            label='Test Cluster',
            centroid=Point(-74.0065, 40.7129, srid=4326),
            scope='plans'
        )
        assert 'Test Cluster' in str(cluster)
        assert 'plans' in str(cluster)


@pytest.mark.django_db
class TestVenueModel:
    """Test Venue model."""
    
    def test_venue_creation(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        partner = Partner.objects.create(
            owner_user=user,
            legal_name='Test Partner LLC',
            status='active'
        )
        venue = Venue.objects.create(
            partner=partner,
            name='Test Venue',
            location=Point(-74.0060, 40.7128, srid=4326),
            status='active'
        )
        assert venue.name == 'Test Venue'
        assert venue.partner == partner
        assert venue.status == 'active'
    
    def test_venue_str(self):
        user = User.objects.create_user(handle='testuser', email='test@example.com', password='test')
        partner = Partner.objects.create(
            owner_user=user,
            legal_name='Test Partner LLC'
        )
        venue = Venue.objects.create(
            partner=partner,
            name='Test Venue',
            location=Point(-74.0060, 40.7128, srid=4326)
        )
        assert str(venue) == 'Test Venue'
