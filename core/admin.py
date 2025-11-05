"""
Admin configuration for the Spontime application.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.gis.admin import GISModelAdmin
from .models import User, Place, Plan, CheckIn, Cluster, Recommendation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio',)}),
    )


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    """Admin for Place model with GIS support."""
    list_display = ['name', 'category', 'address', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'address', 'category']
    gis_widget_kwargs = {
        'attrs': {
            'default_lat': 40.7128,
            'default_lon': -74.0060,
            'default_zoom': 12,
        }
    }


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin for Plan model."""
    list_display = ['title', 'creator', 'place', 'scheduled_time', 'status', 'created_at']
    list_filter = ['status', 'scheduled_time', 'created_at']
    search_fields = ['title', 'description', 'creator__username']
    filter_horizontal = ['participants']
    date_hierarchy = 'scheduled_time'


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """Admin for CheckIn model."""
    list_display = ['user', 'place', 'plan', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'place__name', 'notes']
    date_hierarchy = 'timestamp'


@admin.register(Cluster)
class ClusterAdmin(GISModelAdmin):
    """Admin for Cluster model with GIS support."""
    list_display = ['cluster_id', 'radius', 'created_at', 'place_count']
    list_filter = ['created_at']
    filter_horizontal = ['places']
    
    def place_count(self, obj):
        return obj.places.count()
    place_count.short_description = 'Number of Places'


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin for Recommendation model."""
    list_display = ['user', 'place', 'score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'place__name', 'reason']
    readonly_fields = ['created_at']

