from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


def is_troly(user):
    return user.position.alias == 'tl'

def is_truongphong(user):
    return user.position.alias == 'tp'

def is_giamdoc(user):
    return user.position.alias == 'gd'

class HasHigherPosition(BasePermission):
    message = 'Người dùng phải có chức vụ cao hơn'
    def has_object_permission(self, request, view, obj):
        return request.user.position.id < obj.position.id

class IsOwner(BasePermission):
    message = 'Người dùng phải là chủ sở hữu'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.id == obj.id

class IsNotOwner(BasePermission):
    message = 'Chủ sở hữu không được phép'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.id != obj.id

class InSameDepartment(BasePermission):
    message = 'Người dùng phải thuộc đúng phòng/ban'
    def has_object_permission(self, request, view, obj):
        return request.user.department.id == obj.department.id

class IsGiamdoc(BasePermission):
    message = 'Người dùng phải là giám đốc'
    def has_object_permission(self, request, view, obj):
        return is_giamdoc(request.user)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

class IsTroly(BasePermission):  
    message = 'Người dùng phải là trợ lý'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_troly(request.user)
    
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

class IsTruongPhong(BasePermission):
    message = 'Người dùng phải là trưởng phòng'
    def has_object_permission(self, request, view, obj):
        return is_truongphong(request.user)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)