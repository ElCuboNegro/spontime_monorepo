"""
DRF views for the Spontime application.
"""
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Place, Plan, CheckIn, Cluster, Recommendation
from .serializers import (
    UserSerializer, PlaceSerializer, PlanSerializer,
    CheckInSerializer, ClusterSerializer, RecommendationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet for Place model."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """ViewSet for Plan model with nearby search."""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

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

        # Find plans with places near the point
        nearby_plans = Plan.objects.filter(
            place__location__distance_lte=(point, D(m=radius))
        ).select_related('creator', 'place').prefetch_related('participants')

        serializer = self.get_serializer(nearby_plans, many=True)
        return Response(serializer.data)


class CheckInViewSet(viewsets.ModelViewSet):
    """ViewSet for CheckIn model."""
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter check-ins by user if requested."""
        queryset = CheckIn.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.select_related('user', 'place', 'plan')


class ClusterViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Cluster model."""
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Recommendation model."""
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Get personalized recommendation feed for the current user.
        Returns the latest recommendations ordered by score.
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        recommendations = Recommendation.objects.filter(
            user=request.user
        ).select_related('place').order_by('-score', '-created_at')[:20]

        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)

