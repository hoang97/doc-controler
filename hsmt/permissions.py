import base64, json, hmac, hashlib
from test_hsmt import settings
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_fsm import has_transition_perm
from django.utils import timezone
from hsmt.models import XFile

# Custom permissions

class IsDepartmentAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_DAUTHORIZATION')
        if not token:
            return False
        # giải mã token
        token_data = base64.urlsafe_b64decode(token)
        token_data = json.loads(token_data)
        expiration_time = token_data['exp']
        # Nếu hết tgian hiệu lực => false
        if expiration_time < timezone.now().timestamp():
            return False

        department_id = token_data['department_id']
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if not xfile:
            return False
        department = xfile.department
        # Nếu không đúng phòng của xfile thì không được sửa
        if department_id != department.id:
            return False

        # Kiểm tra chữ kí
        signature_msg = f'{str(expiration_time)}{str(department_id)}{str(department.password)}'
        signature = hmac.new(
            bytes(settings.SECRET_KEY, 'latin-1'),
            msg=bytes(signature_msg, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        if signature != token_data['signature']:
            return False
        return True

class IsNotInUse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.xfile_set.count() == 0

class CanViewXFile(BasePermission):
    def has_permission(self, request, view):
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return xfile.can_view(request.user)
        return False

class CanEditXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.submit_change, request.user)
        return False

class CanSubmitXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.submit_change, request.user)
        return False

class CanCheckXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.check_change, request.user)
        return False

class CanApproveXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.approve_change, request.user)
        return False

class CanRejectCheckXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.reject_check, request.user)
        return False

class CanRejectApproveXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.reject_approve, request.user)
        return False

class CanCreateChangeXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.create_change, request.user)
        return False

class CanCancelChangeXFile(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        xfile_id = request.resolver_match.kwargs.get('pk')
        xfile = XFile.objects.get(id=xfile_id)
        if xfile:
            return has_transition_perm(xfile.cancel_change, request.user)
        return False



