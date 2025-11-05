from rest_framework import serializers
from .models import Message
from users.serializers import UserPublicSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    user = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'plan', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating messages."""
    
    class Meta:
        model = Message
        fields = ['content']
