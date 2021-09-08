import hmac, hashlib, base64, json
from copy import deepcopy
from test_hsmt import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password

from users.models import *
from users.serializers import *
from users.permissions import *
from notifications.utils import notify, VERB


class UserListView(generics.ListAPIView):
    '''
    - fields = ('id', 'username', 'is_active', 'date_joined', 'last_login', 
            'first_name', 'image', 'address', 'skill', 'phone_number', 'self_introduction', 'email', 'layout_config', 
            'department', 'position')

    - read_only_fields = ('username', 'is_active', 'date_joined', 'last_login')
    '''
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''
    - fields = ('id', 'username', 'is_active', 'date_joined', 'last_login', 
            'first_name', 'image', 'address', 'skill', 'phone_number', 'self_introduction', 'email', 'layout_config', 
            'department', 'position')

    - read_only_fields = ('username', 'is_active', 'date_joined', 'last_login')
    '''
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class UserRegisterForOtherView(generics.CreateAPIView):
    '''
    - fields = ('id', 'username', 'first_name', 'password', 'department', 'position')
    - write_only_fields = ('password', )

    User create new account for other:
    - new_user.department = user.department
    - new_user.position less important than user.position
    '''
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Mặc định user được tạo cùng phòng với ng tạo, chức vụ nhỏ hơn
        data = deepcopy(request.data) 
        data['department'] = request.user.department.id
        if not data.get('position') or int(data['position']) < request.user.position.id:
            return Response({'detail': 'Không thể tạo user có chức vụ cao hơn mình'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserRegisterForAnyView(generics.CreateAPIView):
    '''
    - fields = ('id', 'username', 'first_name', 'password', 'department', 'position')
    - write_only_fields = ('password', )

    Create new account for everyone:
    - new_user.position = tro ly
    '''
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [~IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Mặc định user được tạo có chức vụ trợ lí
        data = deepcopy(request.data)
        data['position'] = Position.objects.get(alias='tl').id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserManageView(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('id', 'username', 'first_name', 'is_active', 'position', 'department')'''
    queryset = User.objects.all()
    serializer_class = UserGeneralSerializer
    permission_classes = [IsAuthenticated, IsNotOwner, IsGiamdoc | (InSameDepartment & IsTruongPhong)]

    def update(self, request, *args, **kwargs):
        if not request.data.get('position') or int(request.data['position']) < request.user.position.id:
            return Response({'detail': 'Không thể tạo user có chức vụ cao hơn mình'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

class DepartmentListView(generics.ListAPIView):
    '''fields = ('id', 'name', 'alias')'''
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class PositionListView(generics.ListAPIView):
    '''fields = ('id', 'name', 'alias')'''
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

def department_check_pwd(id, password):
    department = get_object_or_404(Department, id=id)
    return check_password(password, department.password)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTruongPhong])
def department_change_pwd(request):
    '''fields=('department_id', 'password_old', 'password_new')'''
    department_id = request.data.get('department_id')
    password_old = request.data.get('password_old')
    password_new = request.data.get('password_new')
    department = get_object_or_404(Department, id=department_id)

    # chỉ trưởng phòng của phòng tương ứng được đổi
    if request.user.position.alias != 'tp' and request.user.department != department:
        return Response('', status=status.HTTP_403_FORBIDDEN)
    if check_password(password_old, department.password):
        department.password = make_password(password_new)
        department.save()
        return Response('', status= status.HTTP_200_OK)
    return Response('Sai mật khẩu', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def department_login(request):
    '''fields=('department_id', 'password')'''
    department_id = request.data.get('department_id')
    password = request.data.get('password')
    department = get_object_or_404(Department, id=department_id)
    if check_password(password, department.password):
        expiration_time = (timezone.now() + timezone.timedelta(minutes=5)).timestamp()
        signature_msg = f'{str(expiration_time)}{str(department_id)}{str(department.password)}'
        signature = hmac.new(
            bytes(settings.SECRET_KEY, 'latin-1'),
            msg=bytes(signature_msg, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        token_data = {
            'exp': expiration_time,
            'department_id': department_id,
            'signature': signature
        }
        token = base64.urlsafe_b64encode(bytes(json.dumps(token_data), 'latin-1'))
        return Response({'access': token}, status=status.HTTP_200_OK)
    return Response('Sai mật khẩu', status=status.HTTP_400_BAD_REQUEST)