from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


def is_troly(user):
    return user.position.alias == 'tl'

def is_truongphong(user):
    return user.position.alias == 'tp'

def is_giamdoc(user):
    return user.position.alias == 'gd'

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('IsOwner', request.user.id == obj.id)
            return request.user.id == obj.id

class IsNotOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('IsNotOwner', request.user.id != obj.id)
            return request.user.id != obj.id

class InSameDepartment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('InSameDepartment', request.user.department.id == obj.department.id)
            return request.user.department.id == obj.department.id

class IsGiamdoc(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('IsGiamdoc', is_giamdoc(request.user))
            return is_giamdoc(request.user)

class IsTroly(BasePermission):  
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('IsTroly', is_troly(request.user))
            return is_troly(request.user)

class IsTruongPhong(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print('IsTruongPhong', is_truongphong(request.user))
            return is_truongphong(request.user)