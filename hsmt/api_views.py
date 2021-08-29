from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import *

# Support functions
def get_xfiles_can_view(user):
    '''Return a queryset of xfiles that user can view/access'''
    if is_troly(user):
        xfiles_can_edit = user.xfiles_can_edit.all()
        xfiles_can_check = user.xfiles_can_check.all()
        return (xfiles_can_edit | xfiles_can_check).distinct()
    if is_truongphong(user):
        return XFile.objects.filter(department=user.info.department)
    if is_giamdoc(user):
        return XFile.objects.all()

# REST APIs
class XFilePermView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        user = request.user
        xfile = get_object_or_404(XFile, id=pk)
        data = {
            'view': xfile.can_view(user),
            'createChange': has_transition_perm(xfile.create_change, user),
            'edit': has_transition_perm(xfile.submit_change, user),
            'cancel': has_transition_perm(xfile.cancel_change, user),
            'submit': has_transition_perm(xfile.submit_change, user),
            'check': has_transition_perm(xfile.check_change, user),
            'rejectCheck': has_transition_perm(xfile.reject_check, user),
            'approve': has_transition_perm(xfile.approve_change, user),
            'rejectApprove': has_transition_perm(xfile.reject_approve, user),
        }
        return Response(data)

class XFileListView(generics.ListAPIView):
    '''
    - Hiển thị dưới dạng nested dictionary
    - fields = ('id', 'code', 'status', 'version', 'description', 'date_created', 'type', 'targets', 'department', 'creator', 'editors', 'checkers', 'approvers')
    '''
    serializer_class = XFileGeneralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFileCreateView(generics.CreateAPIView):
    '''fields = ('code', 'description', 'type', 'targets', 'editors', 'checkers', 'approvers')'''
    serializer_class = XFileCreateSerializer
    permission_classes = [IsAuthenticated, IsTroly]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class XFileRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    '''
    - Hiển thị dưới dạng nested dictionary
    - fields = ('id', 'code', 'status', 'version', 'description', 'date_created', 'type', 'targets', 'department', 'creator', 'editors', 'checkers', 'approvers')
    '''
    serializer_class = XFileGeneralSerializer
    permission_classes = [IsAuthenticated, IsGiamdoc]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFileGeneralUpdateView(generics.UpdateAPIView):
    '''fields = ('id', 'code', 'description', 'targets', 'editors', 'checkers', 'approvers')'''
    serializer_class = XFileGeneralUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditXFile]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFileContentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''fields = ('id', 'content')
    - Trả ra JSON_dict thể hiện các trường dữ liệu
    - Nhận vào JSON_string để update
    '''
    serializer_class = XFileContentSerializer
    permission_classes = [IsAuthenticated, CanEditXFile]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFileTypeListCreateView(generics.ListCreateAPIView):
    '''fields = ('id', 'name', 'example_content')'''
    queryset = XFileType.objects.all()
    serializer_class = XFileTypeSerializer
    permission_classes = [IsAuthenticated, IsGiamdoc]

class XFileTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('id', 'name', 'example_content')'''
    queryset = XFileType.objects.all()
    serializer_class = XFileTypeSerializer
    permission_classes = [IsAuthenticated, IsGiamdoc]

class TargetListCreateView(generics.ListCreateAPIView):
    ''''''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]

class TargetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    ''''''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]