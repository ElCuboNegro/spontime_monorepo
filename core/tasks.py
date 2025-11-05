"""
Celery tasks for the Spontime application.
"""
import numpy as np
from celery import shared_task
from django.contrib.gis.geos import Point
from django.utils import timezone
from sklearn.cluster import DBSCAN
from .models import Place, Venue, Cluster, CheckIn, RecoSnapshot, RecoItem, Plan, User


@shared_task
def update_clusters():
    """
    Update place/venue clusters using DBSCAN algorithm.
    This task runs periodically to group nearby locations.
    """
    # Cluster places
    places = Place.objects.all()
    if places.count() >= 2:
        _cluster_entities(places, 'places')
    
    # Cluster venues
    venues = Venue.objects.all()
    if venues.count() >= 2:
        _cluster_entities(venues, 'venues')
    
    return "Clustering completed"


def _cluster_entities(queryset, scope):
    """Helper function to cluster entities with location field."""
    # Extract coordinates
    coordinates = []
    entity_ids = []
    
    for entity in queryset:
        lon = entity.location.x
        lat = entity.location.y
        coordinates.append([lat, lon])
        entity_ids.append(entity.id)
    
    # Convert to numpy array
    X = np.array(coordinates)
    
    # Apply DBSCAN clustering
    db = DBSCAN(eps=0.01, min_samples=2).fit(X)
    labels = db.labels_
    
    # Clear existing clusters for this scope
    Cluster.objects.filter(scope=scope).delete()
    
    # Create new clusters
    unique_labels = set(labels)
    cluster_count = 0
    
    for label in unique_labels:
        if label == -1:  # Noise points
            continue
        
        # Get entities in this cluster
        cluster_mask = labels == label
        cluster_coords = X[cluster_mask]
        
        # Calculate centroid
        centroid_lat = float(np.mean(cluster_coords[:, 0]))
        centroid_lon = float(np.mean(cluster_coords[:, 1]))
        centroid = Point(centroid_lon, centroid_lat, srid=4326)
        
        # Create cluster
        cluster = Cluster.objects.create(
            label=f"{scope.capitalize()} Cluster {label}",
            centroid=centroid,
            scope=scope,
            plan_count=0  # Will be updated separately
        )
        cluster_count += 1
    
    return cluster_count


@shared_task
def generate_recommendations():
    """
    Generate personalized recommendations for all users.
    This task runs periodically to update the recommendation feed.
    """
    users = User.objects.filter(is_active=True)
    snapshot_count = 0
    
    for user in users:
        # Get user's check-in history
        user_checkins = CheckIn.objects.filter(user=user).select_related('plan')
        
        if user_checkins.count() == 0:
            continue
        
        # Get plans the user has participated in
        participated_plan_ids = set(checkin.plan_id for checkin in user_checkins)
        
        # Get plans from user's attendances
        from .models import Attendance
        user_attendances = Attendance.objects.filter(user=user, status='joined')
        attended_plan_ids = set(att.plan_id for att in user_attendances)
        
        # Combine all plan IDs the user has been involved with
        all_user_plan_ids = participated_plan_ids | attended_plan_ids
        
        # Get tags from plans user has attended
        user_tags = set()
        for plan in Plan.objects.filter(id__in=all_user_plan_ids):
            if isinstance(plan.tags, list):
                user_tags.update(plan.tags)
        
        # Find upcoming plans that the user hasn't joined
        upcoming_plans = Plan.objects.filter(
            is_active=True,
            starts_at__gte=timezone.now()
        ).exclude(
            id__in=all_user_plan_ids
        ).select_related('host_user', 'place', 'venue')[:50]
        
        if upcoming_plans.count() == 0:
            continue
        
        # Create recommendation snapshot
        snapshot = RecoSnapshot.objects.create(
            user=user,
            algo_version='v1.0',
            explanations=[]
        )
        
        # Score and create recommendation items
        for plan in upcoming_plans[:20]:  # Limit to top 20
            # Calculate score based on tag overlap
            score = 0.5  # Base score
            
            plan_tags = set(plan.tags) if isinstance(plan.tags, list) else set()
            shared_tags = len(user_tags & plan_tags)
            
            if shared_tags > 0:
                score += 0.3 * min(shared_tags / max(len(user_tags), 1), 1.0)
            
            # Calculate distance if user has a location from checkins
            distance_m = 0
            latest_checkin = user_checkins.order_by('-created_at').first()
            if latest_checkin and latest_checkin.geo and (plan.place or plan.venue):
                target_location = plan.place.location if plan.place else plan.venue.location
                distance_m = int(latest_checkin.geo.distance(target_location) * 111000)  # degrees to meters
                
                # Boost score for nearby plans
                if distance_m < 5000:  # Within 5km
                    score += 0.2
            
            # Cap score at 1.0
            score = min(score, 1.0)
            
            # Create recommendation item
            RecoItem.objects.create(
                snapshot=snapshot,
                plan=plan,
                score=score,
                distance_m=distance_m,
                shared_tags=shared_tags
            )
        
        snapshot_count += 1
    
    return f"Generated {snapshot_count} recommendation snapshots for {users.count()} users"
