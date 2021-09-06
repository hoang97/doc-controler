from hsmt.serializers import XFileChangeSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_fsm import has_transition_perm
from hsmt.models import XFile, AttackLog, Comment, XFileChange

# Custom permissions

class IsNotInUse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.xfile_set.count() == 0

class CanViewXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif isinstance(obj, XFile):
            xfile = obj
        elif isinstance(obj, XFileChange):
            xfile = obj.file
        elif isinstance(obj, AttackLog):
            xfile = obj.file
        elif isinstance(obj, Comment):
            xfile = obj.content_object
        else:
            raise Exception('Unexpected type of tagged object')
        return xfile.can_view(request.user)

class CanEditXFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif isinstance(obj, XFile):
            return has_transition_perm(obj.submit_change, request.user)
        elif isinstance(obj, XFileChange):
            return has_transition_perm(obj.file.submit_change, request.user)
        elif isinstance(obj, AttackLog):
            return has_transition_perm(obj.file.submit_change, request.user)
        elif isinstance(obj, Comment):
            return has_transition_perm(obj.content_object.submit_change, request.user)
        else:
            raise Exception('Unexpected type of tagged object')

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



