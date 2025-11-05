"""
Admin configuration for the Spontime application.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.gis.admin import GISModelAdmin
from .models import (
    User, Device, InterestTag, UserInterestTag, Place, Partner, Venue,
    Cluster, Plan, Attendance, JoinRequest, CheckIn, Message, Offer,
    Boost, RecoSnapshot, RecoItem, PopularityCounter, Report,
    ModerationAction, BlockList, AuditLog, Subscription, Invoice
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model."""
    list_display = ['handle', 'email', 'display_name', 'status', 'created_at']
    list_filter = ['status', 'is_staff', 'is_superuser']
    search_fields = ['handle', 'email', 'display_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('handle', 'display_name', 'phone', 'photo_url', 'language')}),
        ('Settings', {'fields': ('privacy_settings', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Admin for Device model."""
    list_display = ['user', 'platform', 'last_seen', 'trust_score']
    list_filter = ['platform']
    search_fields = ['user__handle', 'user__email', 'push_token']


@admin.register(InterestTag)
class InterestTagAdmin(admin.ModelAdmin):
    """Admin for InterestTag model."""
    list_display = ['name', 'slug', 'type']
    search_fields = ['name', 'slug']
    list_filter = ['type']


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    """Admin for Place model with GIS support."""
    list_display = ['name', 'city', 'country', 'owner_user', 'created_at']
    list_filter = ['city', 'country', 'created_at']
    search_fields = ['name', 'address', 'city']
    raw_id_fields = ['owner_user']
    gis_widget_kwargs = {
        'attrs': {
            'default_lat': 40.7128,
            'default_lon': -74.0060,
            'default_zoom': 12,
        }
    }


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Admin for Partner model."""
    list_display = ['legal_name', 'owner_user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['legal_name', 'owner_user__handle']
    raw_id_fields = ['owner_user']


@admin.register(Venue)
class VenueAdmin(GISModelAdmin):
    """Admin for Venue model with GIS support."""
    list_display = ['name', 'partner', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'address', 'partner__legal_name']
    raw_id_fields = ['partner']


@admin.register(Cluster)
class ClusterAdmin(GISModelAdmin):
    """Admin for Cluster model with GIS support."""
    list_display = ['label', 'scope', 'plan_count', 'created_at']
    list_filter = ['scope', 'created_at']
    search_fields = ['label']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin for Plan model."""
    list_display = ['title', 'host_user', 'starts_at', 'visibility', 'is_active', 'created_at']
    list_filter = ['visibility', 'is_active', 'starts_at', 'created_at']
    search_fields = ['title', 'description', 'host_user__handle']
    raw_id_fields = ['host_user', 'venue', 'place', 'cluster']
    date_hierarchy = 'starts_at'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin for Attendance model."""
    list_display = ['user', 'plan', 'status', 'joined_at', 'left_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__handle', 'plan__title']
    raw_id_fields = ['user', 'plan']


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    """Admin for JoinRequest model."""
    list_display = ['user', 'plan', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__handle', 'plan__title']
    raw_id_fields = ['user', 'plan']


@admin.register(CheckIn)
class CheckInAdmin(GISModelAdmin):
    """Admin for CheckIn model."""
    list_display = ['user', 'plan', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__handle', 'plan__title']
    raw_id_fields = ['user', 'plan']
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model."""
    list_display = ['user', 'plan', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__handle', 'plan__title', 'content']
    raw_id_fields = ['user', 'plan']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin for Offer model."""
    list_display = ['title', 'venue', 'valid_from', 'valid_to', 'capacity']
    list_filter = ['valid_from', 'valid_to']
    search_fields = ['title', 'venue__name']
    raw_id_fields = ['venue']


@admin.register(Boost)
class BoostAdmin(admin.ModelAdmin):
    """Admin for Boost model."""
    list_display = ['target_type', 'target_id', 'budget', 'start_at', 'end_at', 'status']
    list_filter = ['target_type', 'status', 'start_at']
    search_fields = ['target_id']


@admin.register(RecoSnapshot)
class RecoSnapshotAdmin(admin.ModelAdmin):
    """Admin for RecoSnapshot model."""
    list_display = ['user', 'algo_version', 'generated_at']
    list_filter = ['generated_at', 'algo_version']
    search_fields = ['user__handle']
    raw_id_fields = ['user']


@admin.register(RecoItem)
class RecoItemAdmin(admin.ModelAdmin):
    """Admin for RecoItem model."""
    list_display = ['snapshot', 'plan', 'score', 'distance_m', 'shared_tags']
    list_filter = ['score']
    search_fields = ['plan__title']
    raw_id_fields = ['snapshot', 'plan']


@admin.register(PopularityCounter)
class PopularityCounterAdmin(admin.ModelAdmin):
    """Admin for PopularityCounter model."""
    list_display = ['key_type', 'key_id', 'window', 'count', 'updated_at']
    list_filter = ['key_type', 'window']
    search_fields = ['key_id']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin for Report model."""
    list_display = ['reporter_user', 'target_type', 'target_id', 'status', 'created_at']
    list_filter = ['target_type', 'status', 'created_at']
    search_fields = ['reporter_user__handle', 'reason', 'target_id']
    raw_id_fields = ['reporter_user']


@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    """Admin for ModerationAction model."""
    list_display = ['admin', 'target_type', 'target_id', 'action', 'created_at']
    list_filter = ['action', 'target_type', 'created_at']
    search_fields = ['admin__handle', 'reason', 'target_id']
    raw_id_fields = ['admin']


@admin.register(BlockList)
class BlockListAdmin(admin.ModelAdmin):
    """Admin for BlockList model."""
    list_display = ['blocker_user', 'blocked_user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker_user__handle', 'blocked_user__handle']
    raw_id_fields = ['blocker_user', 'blocked_user']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model."""
    list_display = ['actor_type', 'actor_id', 'event', 'entity_type', 'entity_id', 'at']
    list_filter = ['actor_type', 'entity_type', 'at']
    search_fields = ['event', 'actor_id', 'entity_id']
    readonly_fields = ['at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin for Subscription model."""
    list_display = ['user', 'partner', 'tier', 'status', 'started_at', 'renewed_at']
    list_filter = ['tier', 'status', 'started_at']
    search_fields = ['user__handle', 'partner__legal_name']
    raw_id_fields = ['user', 'partner']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin for Invoice model."""
    list_display = ['subscription', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['subscription__user__handle', 'provider_ref']
    raw_id_fields = ['subscription']

