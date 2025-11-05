from django.db import models
from django.conf import settings
from django.utils import timezone
from math import radians, cos, sin, asin, sqrt


class InterestTag(models.Model):
    """Tags for categorizing plans by interest."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'interest_tags'
        ordering = ['name']


class Plan(models.Model):
    """A spontaneous plan/event."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_plans'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_plans',
        blank=True
    )
    tags = models.ManyToManyField(InterestTag, related_name='plans', blank=True)
    max_participants = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location_name}"

    def is_happening_soon(self):
        """Check if plan is happening within the next 2 hours."""
        now = timezone.now()
        return self.start_time <= now + timezone.timedelta(hours=2)

    def is_member(self, user):
        """Check if user is a member of this plan."""
        return self.members.filter(id=user.id).exists() or self.creator == user
    
    @property
    def member_count(self):
        """Get total number of members including creator."""
        return self.members.count() + 1  # +1 for creator

    def distance_to(self, lat, lon):
        """
        Calculate distance to a point using Haversine formula.
        Returns distance in kilometers.
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude, lon, lat])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c  # Radius of earth in kilometers
        return km

    class Meta:
        db_table = 'plans'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['start_time', 'is_active']),
            models.Index(fields=['is_active']),
            models.Index(fields=['latitude', 'longitude']),
        ]

