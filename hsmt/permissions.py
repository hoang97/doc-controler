from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_fsm import has_transition_perm

def is_troly(user):
    return user.info.position.alias == 'tl'

def is_truongphong(user):
    return user.info.position.alias == 'tp'

def is_giamdoc(user):
    return user.info.position.alias == 'gd'

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

class IsGiamdoc(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_giamdoc(request.user)

class IsTroly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_troly(request.user)

