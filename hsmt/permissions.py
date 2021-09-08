import base64, json, hmac, hashlib
from test_hsmt import settings
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django_fsm import has_transition_perm
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from hsmt.models import XFile, AttackLog, Comment, XFileChange

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
        xfile = get_object_or_404(XFile, id=xfile_id)
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



