"""
Celery tasks for the Spontime application.
"""
import numpy as np
from celery import shared_task
from django.contrib.gis.geos import Point
from sklearn.cluster import DBSCAN
from .models import Place, Cluster, CheckIn, Recommendation, User


@shared_task
def update_clusters():
    """
    Update place clusters using DBSCAN algorithm.
    This task runs periodically to group nearby places.
    """
    places = Place.objects.all()
    
    if places.count() < 2:
        return "Not enough places to cluster"
    
    # Extract coordinates from places
    coordinates = []
    place_ids = []
    
    for place in places:
        # Convert to lat/lon coordinates
        lon = place.location.x
        lat = place.location.y
        coordinates.append([lat, lon])
        place_ids.append(place.id)
    
    # Convert to numpy array
    X = np.array(coordinates)
    
    # Apply DBSCAN clustering
    # eps is in degrees, roughly 0.01 degree = ~1km at equator
    # min_samples is the minimum number of places to form a cluster
    db = DBSCAN(eps=0.01, min_samples=2).fit(X)
    labels = db.labels_
    
    # Clear existing clusters
    Cluster.objects.all().delete()
    
    # Create new clusters
    unique_labels = set(labels)
    cluster_count = 0
    
    for label in unique_labels:
        if label == -1:  # Noise points
            continue
        
        # Get places in this cluster
        cluster_mask = labels == label
        cluster_place_ids = [place_ids[i] for i, mask in enumerate(cluster_mask) if mask]
        cluster_coords = X[cluster_mask]
        
        # Calculate centroid
        centroid_lat = float(np.mean(cluster_coords[:, 0]))
        centroid_lon = float(np.mean(cluster_coords[:, 1]))
        centroid = Point(centroid_lon, centroid_lat, srid=4326)
        
        # Calculate radius (max distance from centroid)
        distances = np.sqrt(
            (cluster_coords[:, 0] - centroid_lat) ** 2 +
            (cluster_coords[:, 1] - centroid_lon) ** 2
        )
        radius = float(np.max(distances)) * 111000  # Convert degrees to meters
        
        # Create cluster
        cluster = Cluster.objects.create(
            cluster_id=int(label),
            centroid=centroid,
            radius=radius
        )
        cluster.places.set(cluster_place_ids)
        cluster_count += 1
    
    return f"Created {cluster_count} clusters from {len(places)} places"


@shared_task
def generate_recommendations():
    """
    Generate personalized recommendations for all users.
    This task runs periodically to update the recommendation feed.
    """
    users = User.objects.all()
    recommendation_count = 0
    
    for user in users:
        # Get user's check-in history
        user_checkins = CheckIn.objects.filter(user=user).select_related('place')
        
        if user_checkins.count() == 0:
            continue
        
        # Get places the user has visited
        visited_places = set(checkin.place_id for checkin in user_checkins)
        
        # Get categories the user likes (based on check-ins)
        liked_categories = {}
        for checkin in user_checkins:
            category = checkin.place.category
            if category:
                liked_categories[category] = liked_categories.get(category, 0) + 1
        
        # Find clusters containing places the user has visited
        user_clusters = Cluster.objects.filter(places__in=visited_places).distinct()
        
        # Get recommended places from these clusters
        recommended_places = Place.objects.filter(
            clusters__in=user_clusters
        ).exclude(
            id__in=visited_places
        ).distinct()
        
        # Score and create recommendations
        for place in recommended_places[:10]:  # Limit to top 10
            # Calculate score based on category match and cluster membership
            score = 0.5  # Base score
            
            # Boost score if category matches user preferences
            if place.category in liked_categories:
                score += 0.3 * (liked_categories[place.category] / user_checkins.count())
            
            # Boost score based on cluster membership
            common_clusters = place.clusters.filter(id__in=user_clusters).count()
            if common_clusters > 0:
                score += 0.2 * min(common_clusters / 3, 1.0)
            
            # Cap score at 1.0
            score = min(score, 1.0)
            
            # Generate reason
            reasons = []
            if place.category in liked_categories:
                reasons.append(f"You've visited {liked_categories[place.category]} {place.category} places")
            if common_clusters > 0:
                reasons.append(f"Near places you like")
            reason = ". ".join(reasons) if reasons else "Similar to places you've visited"
            
            # Create or update recommendation
            Recommendation.objects.update_or_create(
                user=user,
                place=place,
                defaults={
                    'score': score,
                    'reason': reason,
                }
            )
            recommendation_count += 1
    
    return f"Generated {recommendation_count} recommendations for {users.count()} users"
