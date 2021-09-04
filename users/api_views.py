from rest_framework import generics, status
from rest_framework.response import Response

from .models import *
from .serializers import *
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
        data = request.data
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

    def create(self, request, *args, **kwargs):
        # Mặc định user được tạo có chức vụ trợ lí
        data = request.data
        data['position'] = Position.objects.get(alias='tl')
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