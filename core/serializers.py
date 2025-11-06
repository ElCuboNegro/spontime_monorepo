"""
DRF serializers for the Spontime application.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (
    User, Device, InterestTag, Place, Partner, Venue, Cluster, Plan,
    Attendance, JoinRequest, CheckIn, Message, Offer, RecoSnapshot, RecoItem
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'handle', 'display_name', 'email', 'phone', 'photo_url', 'language', 'status', 'created_at', 'password']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for Device model."""
    
    class Meta:
        model = Device
        fields = ['id', 'user', 'platform', 'push_token', 'last_seen', 'trust_score']
        read_only_fields = ['id', 'last_seen']


class InterestTagSerializer(serializers.ModelSerializer):
    """Serializer for InterestTag model."""
    
    class Meta:
        model = InterestTag
        fields = ['id', 'name', 'slug', 'type']
        read_only_fields = ['id']


class PlaceSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Place model."""
    owner_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Place
        geo_field = 'location'
        fields = ['id', 'name', 'address', 'city', 'country', 'owner_user', 'tags', 'created_at']
        read_only_fields = ['id', 'created_at']


class PartnerSerializer(serializers.ModelSerializer):
    """Serializer for Partner model."""
    owner_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Partner
        fields = ['id', 'owner_user', 'legal_name', 'contact', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class VenueSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Venue model."""
    partner = PartnerSerializer(read_only=True)
    partner_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Venue
        geo_field = 'location'
        fields = ['id', 'partner', 'partner_id', 'name', 'address', 'contact', 'categories', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class ClusterSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Cluster model."""
    
    class Meta:
        model = Cluster
        geo_field = 'centroid'
        fields = ['id', 'label', 'scope', 'plan_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'plan', 'user', 'status', 'joined_at', 'left_at']
        read_only_fields = ['id', 'joined_at']


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model."""
    host_user = UserSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    cluster = ClusterSerializer(read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    
    venue_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    place_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    cluster_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Plan
        fields = [
            'id', 'host_user', 'venue', 'venue_id', 'place', 'place_id', 'title', 'description',
            'tags', 'starts_at', 'ends_at', 'capacity', 'visibility', 'is_active',
            'cluster', 'cluster_id', 'rules', 'attendances', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'host_user', 'created_at', 'updated_at']


class JoinRequestSerializer(serializers.ModelSerializer):
    """Serializer for JoinRequest model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = JoinRequest
        fields = ['id', 'plan', 'user', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CheckInSerializer(serializers.ModelSerializer):
    """Serializer for CheckIn model."""
    user = UserSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = CheckIn
        fields = ['id', 'user', 'plan', 'plan_id', 'geo', 'created_at', 'flags']
        read_only_fields = ['id', 'user', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'plan', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'venue', 'venue_id', 'title', 'description', 'valid_from', 'valid_to', 'tags', 'capacity']
        read_only_fields = ['id']


class RecoItemSerializer(serializers.ModelSerializer):
    """Serializer for RecoItem model."""
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = RecoItem
        fields = ['id', 'plan', 'score', 'distance_m', 'shared_tags']
        read_only_fields = ['id']


class RecoSnapshotSerializer(serializers.ModelSerializer):
    """Serializer for RecoSnapshot model."""
    items = RecoItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = RecoSnapshot
        fields = ['id', 'user', 'generated_at', 'algo_version', 'explanations', 'items']
        read_only_fields = ['id', 'generated_at']
