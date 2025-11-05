from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Plan, InterestTag
from .serializers import PlanSerializer, PlanListSerializer, InterestTagSerializer
from .permissions import IsPlanMember


class InterestTagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for InterestTag model."""
    queryset = InterestTag.objects.all()
    serializer_class = InterestTagSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """ViewSet for Plan model with geospatial filtering."""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsPlanMember]
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'now':
            return PlanListSerializer
        return PlanSerializer
    
    def perform_create(self, serializer):
        """Set creator to current user."""
        plan = serializer.save(creator=self.request.user)
        # Automatically add creator as a member
        plan.members.add(self.request.user)
    
    @action(detail=False, methods=['get'])
    def now(self, request):
        """
        Get active plans happening now or soon, with geospatial filtering.
        
        Query params:
        - lat: Latitude (required)
        - lon: Longitude (required)
        - radius: Search radius in kilometers (default: 2)
        - tags: Comma-separated tag IDs for filtering (optional)
        """
        # Get and validate location parameters
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        
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
                {'error': 'lat and lon must be valid numbers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get radius (default 2 km)
        try:
            radius = float(request.query_params.get('radius', 2))
        except ValueError:
            radius = 2
        
        # Store user location in request for serializer
        request.user_lat = lat
        request.user_lon = lon
        
        # Get current time and time window (next 2 hours)
        now = timezone.now()
        time_window = now + timezone.timedelta(hours=2)
        
        # Base queryset: active plans within time window
        queryset = Plan.objects.filter(
            is_active=True,
            start_time__lte=time_window,
            end_time__gte=now
        )
        
        # Apply tag filtering (OR logic)
        tags = request.query_params.get('tags')
        if tags:
            tag_ids = [int(tid) for tid in tags.split(',') if tid.isdigit()]
            if tag_ids:
                queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        
        # Prefetch related data for efficiency
        queryset = queryset.select_related('creator').prefetch_related('tags', 'members')
        
        # Filter by distance and sort
        plans = []
        for plan in queryset:
            distance = plan.distance_to(lat, lon)
            if distance <= radius:
                plans.append((plan, distance))
        
        # Sort by distance first, then by time proximity
        plans.sort(key=lambda x: (
            x[1],  # Distance
            abs((x[0].start_time - now).total_seconds())  # Time proximity
        ))
        
        # Extract just the plan objects
        plans = [p[0] for p in plans]
        
        # Paginate results
        page = self.paginate_queryset(plans)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[])
    def join(self, request, pk=None):
        """Join a plan."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        plan = self.get_object()
        
        if plan.is_member(request.user):
            return Response(
                {'error': 'You are already a member of this plan'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if plan.members.count() >= plan.max_participants:
            return Response(
                {'error': 'Plan is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.members.add(request.user)
        serializer = self.get_serializer(plan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[])
    def leave(self, request, pk=None):
        """Leave a plan."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        plan = self.get_object()
        
        if plan.creator == request.user:
            return Response(
                {'error': 'Creator cannot leave the plan'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not plan.is_member(request.user):
            return Response(
                {'error': 'You are not a member of this plan'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.members.remove(request.user)
        serializer = self.get_serializer(plan)
        return Response(serializer.data)

