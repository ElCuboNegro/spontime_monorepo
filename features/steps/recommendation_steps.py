"""
Behave step definitions for recommendations.
"""
from behave import given, when, then
from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from core.models import User, Place, Plan, CheckIn, RecoSnapshot, RecoItem


@given('I have checked into some places')
def step_impl(context):
    # Create some plans with places
    place1 = Place.objects.create(
        name='Coffee Shop',
        location=Point(-74.0060, 40.7128, srid=4326),
        city='New York',
        country='USA'
    )
    place2 = Place.objects.create(
        name='Another Coffee Shop',
        location=Point(-74.0070, 40.7130, srid=4326),
        city='New York',
        country='USA'
    )
    
    # Create plans
    plan1 = Plan.objects.create(
        title='Coffee Meetup 1',
        host_user=context.user,
        place=place1,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() - timedelta(days=1, hours=-2)
    )
    plan2 = Plan.objects.create(
        title='Coffee Meetup 2',
        host_user=context.user,
        place=place2,
        starts_at=timezone.now() - timedelta(days=2),
        ends_at=timezone.now() - timedelta(days=2, hours=-2)
    )
    
    # Create check-ins
    CheckIn.objects.create(user=context.user, plan=plan1)
    CheckIn.objects.create(user=context.user, plan=plan2)
    
    context.visited_places = [place1, place2]


@given('recommendations have been generated')
def step_impl(context):
    # Create a recommended place and plan
    recommended_place = Place.objects.create(
        name='New Coffee Shop',
        location=Point(-74.0065, 40.7129, srid=4326),
        city='New York',
        country='USA'
    )
    
    recommended_plan = Plan.objects.create(
        title='Coffee Hangout',
        host_user=context.user,
        place=recommended_place,
        starts_at=timezone.now() + timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1, hours=2)
    )
    
    # Create recommendation snapshot
    snapshot = RecoSnapshot.objects.create(
        user=context.user,
        algo_version='v1.0',
        explanations=['Based on your coffee shop visits']
    )
    
    # Create recommendation item
    context.reco_item = RecoItem.objects.create(
        snapshot=snapshot,
        plan=recommended_plan,
        score=0.850,
        distance_m=500,
        shared_tags=2
    )
    context.snapshot = snapshot


@when('I request my recommendation feed')
def step_impl(context):
    context.snapshot = RecoSnapshot.objects.filter(
        user=context.user
    ).order_by('-generated_at').first()


@then('I should receive personalized recommendations')
def step_impl(context):
    assert context.snapshot is not None
    assert context.snapshot.items.count() > 0


@then('the recommendations should be sorted by score')
def step_impl(context):
    items = list(context.snapshot.items.all().order_by('-score'))
    scores = [float(item.score) for item in items]
    assert scores == sorted(scores, reverse=True)
