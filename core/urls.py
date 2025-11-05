"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PlaceViewSet, VenueViewSet, PlanViewSet,
    AttendanceViewSet, JoinRequestViewSet, CheckInViewSet,
    MessageViewSet, ClusterViewSet, OfferViewSet, RecoSnapshotViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'join-requests', JoinRequestViewSet)
router.register(r'checkins', CheckInViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'recs', RecoSnapshotViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
