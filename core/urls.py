"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PlaceViewSet, PlanViewSet,
    CheckInViewSet, ClusterViewSet, RecommendationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'checkins', CheckInViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'recs', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
