from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with minimal PII exposure."""
    
    class Meta:
        model = User
        fields = ['id', 'handle', 'photo_url', 'username']
        read_only_fields = ['id', 'username']


class UserPublicSerializer(serializers.ModelSerializer):
    """Public serializer for User - pseudonymized."""
    
    class Meta:
        model = User
        fields = ['id', 'handle', 'photo_url']
        read_only_fields = ['id', 'handle', 'photo_url']
