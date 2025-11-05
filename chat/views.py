from rest_framework import viewsets, status
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer
from plans.permissions import IsPlanMemberForMessage
from plans.models import Plan


@method_decorator(ratelimit(key='user', rate='5/m', method='POST'), name='create')
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model with rate limiting.
    
    Rate limit: 5 messages per minute per user.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsPlanMemberForMessage]
    
    def get_queryset(self):
        """Filter messages by plan_id from URL."""
        plan_id = self.kwargs.get('plan_id')
        return Message.objects.filter(plan_id=plan_id).select_related('user', 'plan')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new message for the plan."""
        plan_id = self.kwargs.get('plan_id')
        
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response(
                {'error': 'Plan not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is a member
        if not plan.is_member(request.user):
            return Response(
                {'error': 'Only plan members can post messages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(user=request.user, plan=plan)
        
        # Return full message with user info
        output_serializer = MessageSerializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

