import datetime

from rest_framework import serializers
from hsmt.models import AttackLog, XFile, XFileType, XFileChange, Target, Comment
from users.serializers import DepartmentSerializer, UserGeneralSerializer

# Support functions

def get_change_content(old_content, new_content):
    '''
    - Nhận vào JSON_dict của XFile cũ và mới
    - Đưa ra JSON_dict thể hiện sự thay đổi
    - 2 XFile phải cùng kiểu hồ sơ (type)
    '''
    change = {}
    
    key1 = set(old_content.keys())
    key2 = set(new_content.keys())

    # Với mỗi trường trong tổng hợp nội dung cả 2 file, kiểm tra sự khác nhau
    for field in key1 | key2 :
        old_record = old_content.get(field)
        new_record = new_content.get(field)
        if old_record != new_record:
            change[field] = {
                'type': new_record.get('type'),
                'old' : old_record.get('value'),
                'new' : new_record.get('value')
            }
    
    return change

def get_old_xfile_content(xfile):
    if xfile.version == 0:
        # Nếu XFile đang trong trạng thái khởi tạo thì ko thể update
        raise ValueError("Can't update XFile in INIT status")
    old_xfile = xfile.get_xfile_by_version(xfile.version-1)
    old_content = old_xfile.get_xfile_content()
    return old_content

def save_to_xfile_change(xfile, old_content, new_content):
    change_content = get_change_content(old_content, new_content)
    change = xfile.changes.get(version=xfile.version)
    change.update(change_content)

# Serializers

class CommentSerializer(serializers.ModelSerializer):
    author = UserGeneralSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'date_created')
        read_only_fields = ('id', 'date_created')

class CommentGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'date_created', 'content_type', 'object_id')
        read_only_fields = ('id', 'date_created')

class AttackLogSerializer(serializers.ModelSerializer):
    attacker = UserGeneralSerializer()
    class Meta:
        model = AttackLog
        fields = ('id', 'timestamp', 'process', 'result', 'attacker', 'file')

class AttackLogGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackLog
        fields = ('id', 'timestamp', 'process', 'result', 'attacker', 'file')

class XFileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFileType
        fields = ('id', 'name', 'example_content')

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'name', 'description', 'get_type_display', 'type')

class XFileChangeSerializer(serializers.ModelSerializer):
    editor = UserGeneralSerializer(read_only=True)
    checker = UserGeneralSerializer(read_only=True)
    approver = UserGeneralSerializer(read_only=True)
    date_edited = serializers.DateField(read_only=True)
    
    class Meta:
        model = XFileChange
        fields = ('id', 'name', 'content', 'date_created', 'date_edited', 'editor', 'checker', 'approver')
        read_only_fields = ('id', 'content', 'date_created', 'date_edited', 'editor', 'checker', 'approver')

class XFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFile
        fields = ('code', 'description', 'type', 'targets', 'department', 'creator', 'editors', 'checkers', 'approvers', 'content')

class XFileGeneralSerializer(serializers.ModelSerializer):
    type = XFileTypeSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    creator = UserGeneralSerializer(read_only=True)
    targets = TargetSerializer(many=True)
    editors = UserGeneralSerializer(many=True)
    checkers = UserGeneralSerializer(many=True)
    approvers = UserGeneralSerializer(many=True)
    # comments = CommentSerializer(many=True)

    class Meta:
        model = XFile
        fields = ('id', 'code', 'status', 'get_status_display', 'version', 'description', 'date_created', 'type', 'targets', 'department', 'creator', 'editors', 'checkers', 'approvers')
        read_only_fields = ('id', 'status', 'get_status_display', 'version', 'date_created', 'department', 'creator')

class XFilePermUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFile
        fields = ('id', 'editors', 'checkers', 'approvers')

class XFileGeneralUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFile
        fields = ('id', 'code', 'description', 'targets')

class XFileContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFile
        fields = ('id', 'content')
