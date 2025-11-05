"""
DRF serializers for the Spontime application.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import User, Place, Plan, CheckIn, Cluster, Recommendation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']


class PlaceSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Place model."""
    
    class Meta:
        model = Place
        geo_field = 'location'
        fields = ['id', 'name', 'description', 'address', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model."""
    creator = UserSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'description', 'creator', 'place', 'place_id',
            'participants', 'participant_ids', 'scheduled_time', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        plan = Plan.objects.create(**validated_data)
        if participant_ids:
            plan.participants.set(participant_ids)
        return plan

    def update(self, instance, validated_data):
        participant_ids = validated_data.pop('participant_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if participant_ids is not None:
            instance.participants.set(participant_ids)
        return instance


class CheckInSerializer(serializers.ModelSerializer):
    """Serializer for CheckIn model."""
    user = UserSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True)
    plan_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = CheckIn
        fields = ['id', 'user', 'place', 'place_id', 'plan_id', 'timestamp', 'notes']
        read_only_fields = ['id', 'user', 'timestamp']


class ClusterSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Cluster model."""
    places = PlaceSerializer(many=True, read_only=True)
    place_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cluster
        geo_field = 'centroid'
        fields = ['id', 'cluster_id', 'places', 'place_count', 'radius', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_place_count(self, obj):
        return obj.places.count()


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model."""
    place = PlaceSerializer(read_only=True)
    
    class Meta:
        model = Recommendation
        fields = ['id', 'place', 'score', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']
