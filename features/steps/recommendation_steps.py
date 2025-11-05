"""
Behave step definitions for recommendations.
"""
from behave import given, when, then
from django.contrib.gis.geos import Point
from core.models import User, Place, CheckIn, Recommendation


@given('I have checked into some places')
def step_impl(context):
    # Create some places
    place1 = Place.objects.create(
        name='Coffee Shop',
        location=Point(-74.0060, 40.7128, srid=4326),
        category='cafe'
    )
    place2 = Place.objects.create(
        name='Another Coffee Shop',
        location=Point(-74.0070, 40.7130, srid=4326),
        category='cafe'
    )
    
    # Create check-ins
    CheckIn.objects.create(user=context.user, place=place1)
    CheckIn.objects.create(user=context.user, place=place2)
    
    context.visited_places = [place1, place2]


@given('recommendations have been generated')
def step_impl(context):
    # Create a recommended place
    recommended_place = Place.objects.create(
        name='New Coffee Shop',
        location=Point(-74.0065, 40.7129, srid=4326),
        category='cafe'
    )
    
    # Create recommendation
    context.recommendation = Recommendation.objects.create(
        user=context.user,
        place=recommended_place,
        score=0.85,
        reason='Similar to places you have visited'
    )


@when('I request my recommendation feed')
def step_impl(context):
    context.recommendations = Recommendation.objects.filter(
        user=context.user
    ).order_by('-score', '-created_at')


@then('I should receive personalized recommendations')
def step_impl(context):
    assert context.recommendations.count() > 0


@then('the recommendations should be sorted by score')
def step_impl(context):
    scores = [rec.score for rec in context.recommendations]
    assert scores == sorted(scores, reverse=True)
