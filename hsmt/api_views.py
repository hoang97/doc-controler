from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import *
from .serializers import *
from .permissions import *
from notifications.utils import notify, VERB

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
# Để giảm chi phí kiểm tra permission CanView cho từng XFile, 
# thay queryset của các view liên quan đến XFile bằng get_xfiles_can_view(self.request.user)
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanCreateChangeXFile])
def create_change_xfile(request, pk):
    change_name = request.POST.get("change_name","")
    if not change_name:
        return Response({'msg': 'change_name cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
    xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
    user = request.user
    
    xfile.create_change(change_name, by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.CHANGE.label, notify_to=list(xfile.editors.all()))
    return Response('success')
   

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanCancelChangeXFile])
def cancel_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
    user = request.user
    xfile.cancel_change(by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.CANCLE_CHANGE.label, notify_to=list(xfile.editors.all()))
    return Response('success')

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanSubmitXFile])
def submit_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)
    user = request.user
    xfile.submit_change(by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.SEND.label, notify_to=list(xfile.checkers.all()))
    return Response('success')

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanCheckXFile])
def check_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('approvers'), id=pk)
    user = request.user
    xfile.check_change(by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.CHECK.label, notify_to=list(xfile.approvers.all()))
    return Response('success')

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanRejectCheckXFile])
def reject_check_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
    user = request.user
    xfile.reject_check(by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.REJECT_CHECK.label, notify_to=list(xfile.editors.all()))
    return Response('success')

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanApproveXFile])
def approve_change_xfile(request, pk):
    xfile = get_object_or_404(XFile, id=pk)
    user = request.user
    xfile.approve_change(by=user)
    xfile.save()
    notify(
        actor=user, target=xfile, verb=VERB.APPROVE.label, 
        notify_to=list(User.objects.filter(info__department__alias='giamdoc'))
    )
    return Response('success')

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanRejectApproveXFile])
def reject_approve_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)
    user = request.user
    xfile.reject_approve(by=user)
    xfile.save()
    notify(actor=user, target=xfile, verb=VERB.REJECT_APPROVE.label, notify_to=list(xfile.checkers.all()))
    return Response('success')

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
    '''fields = ('id', 'name', 'description', 'get_type_display', 'type')'''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]

class TargetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('id', 'name', 'description', 'get_type_display', 'type')'''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]