from django.contrib import admin
from .models import Plan, InterestTag


@admin.register(InterestTag)
class InterestTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'location_name', 'start_time', 'creator', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_time']
    search_fields = ['title', 'description', 'location_name']
    filter_horizontal = ['members', 'tags']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'creator', 'is_active')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'location_name')
        }),
        ('Time', {
            'fields': ('start_time', 'end_time')
        }),
        ('Participants', {
            'fields': ('members', 'max_participants')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
