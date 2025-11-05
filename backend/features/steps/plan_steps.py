"""
Behave step definitions for plan management.
"""
from behave import given, when, then
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan


@given('I am an authenticated user')
def step_impl(context):
    context.user = User.objects.create_user(
        handle='testuser',
        email='test@example.com',
        password='testpass123'
    )


@given('there is a place available')
def step_impl(context):
    context.place = Place.objects.create(
        name='Test Place',
        location=Point(-74.0060, 40.7128, srid=4326),
        address='123 Test St',
        city='New York',
        country='USA'
    )


@when('I create a plan for that place')
def step_impl(context):
    context.plan = Plan.objects.create(
        title='Test Plan',
        description='A test plan',
        host_user=context.user,
        place=context.place,
        starts_at=timezone.now() + timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1, hours=2),
        is_active=True
    )


@then('the plan should be created successfully')
def step_impl(context):
    assert context.plan.id is not None


@then('the plan should have the correct details')
def step_impl(context):
    assert context.plan.title == 'Test Plan'
    assert context.plan.host_user == context.user
    assert context.plan.place == context.place


@given('there are multiple plans in different locations')
def step_impl(context):
    user = User.objects.create_user(handle='testuser2', email='test2@example.com', password='test')
    
    # Create places at different locations
    place1 = Place.objects.create(
        name='Nearby Place',
        location=Point(-74.0060, 40.7128, srid=4326),  # NYC
        city='New York',
        country='USA'
    )
    place2 = Place.objects.create(
        name='Far Place',
        location=Point(-118.2437, 34.0522, srid=4326),  # LA
        city='Los Angeles',
        country='USA'
    )
    
    # Create plans
    Plan.objects.create(
        title='Nearby Plan',
        description='Close by',
        host_user=user,
        place=place1,
        starts_at=timezone.now() + timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1, hours=2)
    )
    Plan.objects.create(
        title='Far Plan',
        description='Far away',
        host_user=user,
        place=place2,
        starts_at=timezone.now() + timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1, hours=2)
    )
    
    context.nearby_location = (-74.0060, 40.7128)


@when('I search for plans near a specific location')
def step_impl(context):
    from django.contrib.gis.measure import D
    from django.contrib.gis.geos import Point
    
    lat, lon = context.nearby_location
    point = Point(lon, lat, srid=4326)
    context.nearby_plans = Plan.objects.filter(
        place__location__distance_lte=(point, D(m=5000))
    )


@then('I should receive only plans within the specified radius')
def step_impl(context):
    assert context.nearby_plans.count() > 0
    # Check that the nearby plan is in the results
    assert any(plan.title == 'Nearby Plan' for plan in context.nearby_plans)
    assert context.plan.creator == context.user
    assert context.plan.place == context.place


@given('there are multiple plans in different locations')
def step_impl(context):
    user = User.objects.create_user(username='testuser2', password='test')
    
    # Create places at different locations
    place1 = Place.objects.create(
        name='Nearby Place',
        location=Point(-74.0060, 40.7128, srid=4326),  # NYC
        category='restaurant'
    )
    place2 = Place.objects.create(
        name='Far Place',
        location=Point(-118.2437, 34.0522, srid=4326),  # LA
        category='restaurant'
    )
    
    # Create plans
    Plan.objects.create(
        title='Nearby Plan',
        description='Close by',
        creator=user,
        place=place1,
        scheduled_time=timezone.now() + timedelta(days=1)
    )
    Plan.objects.create(
        title='Far Plan',
        description='Far away',
        creator=user,
        place=place2,
        scheduled_time=timezone.now() + timedelta(days=1)
    )
    
    context.nearby_location = (-74.0060, 40.7128)


@when('I search for plans near a specific location')
def step_impl(context):
    from django.contrib.gis.measure import D
    from django.contrib.gis.geos import Point
    
    lat, lon = context.nearby_location
    point = Point(lon, lat, srid=4326)
    context.nearby_plans = Plan.objects.filter(
        place__location__distance_lte=(point, D(m=5000))
    )


@then('I should receive only plans within the specified radius')
def step_impl(context):
    assert context.nearby_plans.count() > 0
    # Check that the nearby plan is in the results
    assert any(plan.title == 'Nearby Plan' for plan in context.nearby_plans)
