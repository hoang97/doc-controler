from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from hsmt.models import *
from hsmt.serializers import *
from hsmt.permissions import *
from users.permissions import *
from notifications.utils import notify, VERB

# Support functions
def get_xfiles_can_view(user):
    '''Return a queryset of xfiles that user can view/access'''
    if is_troly(user):
        xfiles_can_edit = user.xfiles_can_edit.all()
        xfiles_can_check = user.xfiles_can_check.all()
        return (xfiles_can_edit | xfiles_can_check).distinct()
    if is_truongphong(user):
        return XFile.objects.filter(department=user.department)
    if is_giamdoc(user):
        return XFile.objects.all()

# REST APIs
# Để giảm chi phí kiểm tra permission CanView cho từng XFile, 
# thay queryset của các view liên quan đến XFile bằng get_xfiles_can_view(self.request.user)
class XFilePermView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
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
        return Response(data, status.HTTP_200_OK)

class XFileChangeCreateView(APIView):
    permission_classes = [IsAuthenticated, CanCreateChangeXFile]
    http_method_names = ['put']

    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        change_name = request.data.get("change_name","")
        if not change_name:
            return Response({'detail': 'Tên bản cập nhật không được để trống'}, status.HTTP_400_BAD_REQUEST)
        xfile.create_change(change_name, by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.CHANGE.label, notify_to=list(xfile.editors.all()))
        return Response({'detail': 'Tạo bản cập nhật mới thành công'}, status.HTTP_200_OK)
   
class XFileChangeCancelView(APIView):
    permission_classes = [IsAuthenticated, CanCancelChangeXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.cancel_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.CANCLE_CHANGE.label, notify_to=list(xfile.editors.all()))
        return Response({'detail': 'Hủy bản cập nhật thành công'}, status.HTTP_200_OK)
   
class XFileChangeSubmitView(APIView):
    permission_classes = [IsAuthenticated, CanSubmitXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.submit_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.SEND.label, notify_to=list(xfile.checkers.all()))
        return Response({'detail': 'Gửi kiểm định thành công'}, status.HTTP_200_OK)
   
class XFileChangeCheckView(APIView):
    permission_classes = [IsAuthenticated, CanCheckXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('approvers'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.check_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.CHECK.label, notify_to=list(xfile.approvers.all()))
        return Response({'detail': 'Kiểm định thành công'}, status.HTTP_200_OK)
   
class XFileChangeRejectCheckView(APIView):
    permission_classes = [IsAuthenticated, CanRejectCheckXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.reject_check(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.REJECT_CHECK.label, notify_to=list(xfile.editors.all()))
        return Response({'detail': 'Đã yêu cầu sửa lại'}, status.HTTP_200_OK)
   
class XFileChangeApproveView(APIView):
    permission_classes = [IsAuthenticated, CanApproveXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile, id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.approve_change(by=user)
        xfile.save()
        notify(
            actor=user, target=xfile, verb=VERB.APPROVE.label, 
            notify_to=list(User.objects.filter(department__alias='giamdoc'))
        )
        return Response({'detail': 'Phê duyệt thành công'}, status.HTTP_200_OK)
   
class XFileChangeRejectApproveView(APIView):
    permission_classes = [IsAuthenticated, CanRejectApproveXFile]
    http_method_names = ['put']
    
    def get_object(self, pk):
        return get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)

    def put(self, request, pk):
        xfile = self.get_object(pk)
        user = request.user
        self.check_object_permissions(request, xfile)
        xfile.reject_approve(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.REJECT_APPROVE.label, notify_to=list(xfile.checkers.all()))
        return Response({'detail': 'Đã yêu cầu kiểm định lại'}, status.HTTP_200_OK)

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

    # Ghi đè function create để khởi tạo giá trị mặc định cho XFile
    def create(self, request, *args, **kwargs):
        request.data['department'] = request.user.department.id
        request.data['creator'] = request.user.id
        if not request.data.get('type'):
            return Response('Thiếu loại hồ sơ', status.HTTP_400_BAD_REQUEST)
        request.data['content'] = XFileType.objects.get(id = request.data['type']).example_content
        return super().create(request, *args, **kwargs)

class XFileRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    '''
    - Hiển thị dưới dạng nested dictionary
    - fields = ('id', 'code', 'status', 'version', 'description', 'date_created', 'type', 'targets', 'department', 'creator', 'editors', 'checkers', 'approvers')
    '''
    serializer_class = XFileGeneralSerializer
    permission_classes = [IsAuthenticated, IsGiamdoc]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFilePermUpdateView(generics.UpdateAPIView):
    '''fields = ('id', 'editors', 'checkers', 'approvers')'''
    serializer_class = XFilePermUpdateSerializer
    permission_classes = [IsAuthenticated, IsTruongPhong]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

class XFileGeneralUpdateView(generics.UpdateAPIView):
    '''fields = ('id', 'code', 'description', 'targets')'''
    serializer_class = XFileGeneralUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditXFile]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)
    
    # Ghi đè function perform_update để cập nhật XFileChange
    def perform_update(self, serializer):
        instance = self.get_object()
        old_content = get_old_xfile_content(instance)
        new_instance = serializer.save()
        new_content = new_instance.get_xfile_content()
        save_to_xfile_change(instance, old_content, new_content)

class XFileCommentListView(generics.ListAPIView):
    '''fields = ('id', 'author', 'body', 'date_created')'''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanViewXFile]

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.comments

class XFileCommentCreateView(generics.CreateAPIView):
    '''fields = ('body')'''
    serializer_class = CommentGeneralSerializer
    permission_classes = [IsAuthenticated, CanViewXFile]

    # Ghi đè function create để khởi tạo giá trị mặc định cho Comment
    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        request.data['content_type'] = ContentType.objects.get_for_model(XFile).id
        request.data['object_id'] = self.kwargs['pk']
        return super().create(request, *args, **kwargs)

class XFileCommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('body')'''
    serializer_class = CommentGeneralSerializer
    permission_classes = [IsAuthenticated, CanViewXFile]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.comments

    # Ghi đè function update để khởi tạo giá trị mặc định cho Comment
    def update(self, request, *args, **kwargs):
        request.data['author'] = self.get_object().author.id
        request.data['content_type'] = ContentType.objects.get_for_model(XFile).id
        request.data['object_id'] = self.kwargs['pk']
        return super().update(request, *args, **kwargs)


# Cần có mật khẩu phòng mới sử dụng đc

class AttackLogListView(generics.ListAPIView):
    '''fields = ('id', 'timestamp', 'process', 'result', 'attacker', 'file')'''
    serializer_class = AttackLogSerializer
    permission_classes = [IsAuthenticated, CanViewXFile, IsDepartmentAuthenticated]

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.attack_logs.all()

class AttackLogCreateView(generics.CreateAPIView):
    '''fields = ('timestamp', 'process', 'result', 'attacker')'''
    serializer_class = AttackLogGeneralSerializer
    permission_classes = [IsAuthenticated, CanViewXFile, CanEditXFile, IsDepartmentAuthenticated]
    
    # Ghi đè function create để khởi tạo giá trị mặc định cho AttackLog
    def create(self, request, *args, **kwargs):
        request.data['file'] = self.kwargs['pk']
        return super().create(request, *args, **kwargs)

    # Ghi đè function perform_create để cập nhật XFileChange
    def perform_create(self, serializer):
        instance = get_object_or_404(XFile, id=self.kwargs['pk'])
        old_content = get_old_xfile_content(instance)
        new_instance = serializer.save().file
        new_content = new_instance.get_xfile_content()
        save_to_xfile_change(instance, old_content, new_content)

class AttackLogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('id', 'timestamp', 'process', 'result', 'attacker', 'file')'''
    serializer_class = AttackLogGeneralSerializer
    permission_classes = [IsAuthenticated, CanViewXFile, CanEditXFile, IsDepartmentAuthenticated]
    lookup_url_kwarg = 'attacklog_id'

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.attack_logs.all()
    
    # Ghi đè function perform_destroy để cập nhật XFileChange
    def perform_destroy(self, instance):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        old_content = get_old_xfile_content(xfile)
        instance.delete()
        new_content = xfile.get_xfile_content()
        save_to_xfile_change(xfile, old_content, new_content)

class XFileChangeListView(generics.ListAPIView):
    '''fields = ('id', 'name', 'content', 'date_created', 'date_edited', 'editor', 'checker', 'approver')'''
    serializer_class = XFileChangeSerializer
    permission_classes = [IsAuthenticated, CanViewXFile, IsDepartmentAuthenticated]

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.changes.all()

class XFileChangeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''fields = ('id', 'name', 'content', 'date_created', 'date_edited', 'editor', 'checker', 'approver')'''
    serializer_class = XFileChangeSerializer
    permission_classes = [IsAuthenticated, CanViewXFile, CanEditXFile, IsDepartmentAuthenticated]
    lookup_field = 'version'
    lookup_url_kwarg = 'version'

    def get_queryset(self):
        xfile = get_object_or_404(XFile, id=self.kwargs['pk'])
        return xfile.changes.all()

class XFileContentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''fields = ('id', 'content')
    - Content nhận vào JSON_string để update
    - Content trả ra JSON_dict thể hiện các trường dữ liệu
    '''
    serializer_class = XFileContentSerializer
    permission_classes = [IsAuthenticated, CanEditXFile, IsDepartmentAuthenticated]

    def get_queryset(self):
        return get_xfiles_can_view(self.request.user)

    # Ghi đè function perform_update để cập nhật XFileChange
    def perform_update(self, serializer):
        instance = self.get_object()
        old_content = get_old_xfile_content(instance)
        new_instance = serializer.save()
        new_content = new_instance.get_xfile_content()
        save_to_xfile_change(instance, old_content, new_content)

# chỉ giám đốc có quyền sửa, xóa

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

# Ai cx có quyền xem, sửa, xóa

class TargetListCreateView(generics.ListCreateAPIView):
    '''fields = ('id', 'name', 'description', 'get_type_display', 'type')'''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]

class TargetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''fields = ('id', 'name', 'description', 'get_type_display', 'type')'''
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated, IsNotInUse]