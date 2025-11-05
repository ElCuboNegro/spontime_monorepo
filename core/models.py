"""
Models for the Spontime application.
"""
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models


class User(AbstractUser):
    """Custom user model with additional fields."""
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Place(models.Model):
    """Place model with PostGIS Point field."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = gis_models.PointField(geography=True, srid=4326)
    address = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'places'
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name


class Plan(models.Model):
    """Plan model for organizing events."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_plans')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='plans')
    participants = models.ManyToManyField(User, related_name='plans', blank=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plans'
        ordering = ['-scheduled_time']
        indexes = [
            models.Index(fields=['status', 'scheduled_time']),
            models.Index(fields=['creator']),
        ]

    def __str__(self):
        return self.title


class CheckIn(models.Model):
    """Check-in model to track user visits to places."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkins')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='checkins')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkins')
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'checkins'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['place', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} @ {self.place.name}"


class Cluster(models.Model):
    """Cluster model for DBSCAN clustering results."""
    cluster_id = models.IntegerField()
    places = models.ManyToManyField(Place, related_name='clusters')
    centroid = gis_models.PointField(geography=True, srid=4326)
    radius = models.FloatField(help_text='Radius in meters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clusters'
        ordering = ['cluster_id']
        indexes = [
            models.Index(fields=['cluster_id']),
        ]

    def __str__(self):
        return f"Cluster {self.cluster_id}"


class Recommendation(models.Model):
    """Recommendation model for personalized place suggestions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(help_text='Recommendation score (0-1)')
    reason = models.TextField(blank=True, help_text='Explanation for recommendation')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommendations'
        ordering = ['-score', '-created_at']
        unique_together = [['user', 'place', 'created_at']]
        indexes = [
            models.Index(fields=['user', '-score']),
        ]

    def __str__(self):
        return f"{self.place.name} for {self.user.username} (score: {self.score:.2f})"

