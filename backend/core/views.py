"""
DRF views for the Spontime application.
"""
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    User, Place, Venue, Plan, CheckIn, Cluster, Attendance,
    JoinRequest, Message, Offer, RecoSnapshot
)
from .serializers import (
    UserSerializer, PlaceSerializer, VenueSerializer, PlanSerializer,
    CheckInSerializer, ClusterSerializer, AttendanceSerializer,
    JoinRequestSerializer, MessageSerializer, OfferSerializer,
    RecoSnapshotSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet for Place model."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class VenueViewSet(viewsets.ModelViewSet):
    """ViewSet for Venue model."""
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """ViewSet for Plan model with nearby search."""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        serializer.save(host_user=self.request.user)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Get plans near a specific location.
        Query params:
        - lat: latitude
        - lon: longitude
        - radius: radius in meters (default: 5000)
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = int(request.query_params.get('radius', 5000))

        if not lat or not lon:
            return Response(
                {'error': 'lat and lon parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response(
                {'error': 'Invalid lat or lon values'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a point from coordinates
        point = Point(lon, lat, srid=4326)

        # Find plans with places or venues near the point
        nearby_plans = Plan.objects.filter(
            models.Q(place__location__distance_lte=(point, D(m=radius))) |
            models.Q(venue__location__distance_lte=(point, D(m=radius)))
        ).select_related('host_user', 'place', 'venue', 'cluster').prefetch_related('attendances')

        serializer = self.get_serializer(nearby_plans, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Attendance model."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        """Filter attendances by plan or user if requested."""
        queryset = Attendance.objects.all()
        plan_id = self.request.query_params.get('plan_id')
        user_id = self.request.query_params.get('user_id')
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.select_related('user', 'plan')


class JoinRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for JoinRequest model."""
    queryset = JoinRequest.objects.all()
    serializer_class = JoinRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter join requests by plan or user if requested."""
        queryset = JoinRequest.objects.all()
        plan_id = self.request.query_params.get('plan_id')
        user_id = self.request.query_params.get('user_id')
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.select_related('user', 'plan')


class CheckInViewSet(viewsets.ModelViewSet):
    """ViewSet for CheckIn model."""
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter check-ins by user or plan if requested."""
        queryset = CheckIn.objects.all()
        user_id = self.request.query_params.get('user_id')
        plan_id = self.request.query_params.get('plan_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
        return queryset.select_related('user', 'plan')


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter messages by plan if requested."""
        queryset = Message.objects.all()
        plan_id = self.request.query_params.get('plan_id')
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
        return queryset.select_related('user', 'plan').order_by('created_at')


class ClusterViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Cluster model."""
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for Offer model."""
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_queryset(self):
        """Filter offers by venue if requested."""
        queryset = Offer.objects.all()
        venue_id = self.request.query_params.get('venue_id')
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)
        return queryset.select_related('venue')


class RecoSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Recommendation snapshots."""
    queryset = RecoSnapshot.objects.all()
    serializer_class = RecoSnapshotSerializer

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Get personalized recommendation feed for the current user.
        Returns the latest recommendation snapshot.
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get the latest snapshot for the user
        snapshot = RecoSnapshot.objects.filter(
            user=request.user
        ).select_related('user').prefetch_related('items__plan').order_by('-generated_at').first()

        if not snapshot:
            return Response(
                {'message': 'No recommendations available yet'},
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(snapshot)
        return Response(serializer.data)

