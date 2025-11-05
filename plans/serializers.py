from rest_framework import serializers
from .models import Plan, InterestTag
from users.serializers import UserPublicSerializer


class InterestTagSerializer(serializers.ModelSerializer):
    """Serializer for InterestTag model."""
    
    class Meta:
        model = InterestTag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model."""
    creator = UserPublicSerializer(read_only=True)
    members = UserPublicSerializer(many=True, read_only=True)
    tags = InterestTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=InterestTag.objects.all(),
        write_only=True,
        required=False,
        source='tags'
    )
    distance = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'description', 'latitude', 'longitude', 'location_name',
            'start_time', 'end_time', 'creator', 'members', 'tags', 'tag_ids',
            'max_participants', 'is_active', 'created_at', 'updated_at',
            'distance', 'member_count', 'is_joined'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def get_distance(self, obj):
        """Get distance from user's location if available."""
        request = self.context.get('request')
        if request and hasattr(request, 'user_lat') and hasattr(request, 'user_lon'):
            return round(obj.distance_to(request.user_lat, request.user_lon), 2)
        return None
    
    def get_member_count(self, obj):
        """Get total number of members including creator."""
        return obj.members.count() + 1  # +1 for creator
    
    def get_is_joined(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_member(request.user)
        return False


class PlanListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for plan list view."""
    creator = UserPublicSerializer(read_only=True)
    tags = InterestTagSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'description', 'location_name',
            'start_time', 'end_time', 'creator', 'tags',
            'max_participants', 'distance', 'member_count'
        ]
    
    def get_distance(self, obj):
        """Get distance from user's location if available."""
        request = self.context.get('request')
        if request and hasattr(request, 'user_lat') and hasattr(request, 'user_lon'):
            return round(obj.distance_to(request.user_lat, request.user_lon), 2)
        return None
    
    def get_member_count(self, obj):
        """Get total number of members including creator."""
        return obj.members.count() + 1
