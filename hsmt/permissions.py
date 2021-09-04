from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_fsm import has_transition_perm

# Custom permissions
class CanEditXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.submit_change, request.user)

class CanSubmitXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.submit_change, request.user)

class CanCheckXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.check_change, request.user)

class CanApproveXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.approve_change, request.user)

class CanRejectCheckXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.reject_check, request.user)

class CanRejectApproveXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.reject_approve, request.user)

class CanCreateChangeXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.create_change, request.user)

class CanCancelChangeXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return has_transition_perm(obj.cancel_change, request.user)



