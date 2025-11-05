from rest_framework import permissions


class IsPlanMember(permissions.BasePermission):
    """
    Permission to check if user is a member of the plan.
    Allows read access to all, but write access only to members.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for plan members
        return obj.is_member(request.user)


class IsPlanMemberForMessage(permissions.BasePermission):
    """
    Permission to check if user is a member of the plan for messaging.
    """
    
    def has_permission(self, request, view):
        # User must be authenticated
        if not request.user.is_authenticated:
            return False
        
        # For list/create, check if user is member of the plan
        plan_id = view.kwargs.get('plan_id')
        if plan_id:
            from plans.models import Plan
            try:
                plan = Plan.objects.get(id=plan_id)
                return plan.is_member(request.user)
            except Plan.DoesNotExist:
                return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if user is member of the plan
        return obj.plan.is_member(request.user)
