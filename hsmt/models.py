from copy import deepcopy
import json
import logging
from datetime import datetime, date
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import Department
from .utils import decode, notify, VERB
from django_fsm import transition, GET_STATE, FSMIntegerField

# Choices
class STATUS(models.IntegerChoices):
    '''
    Những trạng thái của XFile
    '''
    INIT = 0, _('khởi tạo')
    EDITING = 1, _('đang sửa đổi')
    CHECKING = 2, _('đang kiểm định')
    APPROVING = 3, _('đang phê duyệt')
    DONE = 4, _('đã hoàn thiện')
    
class TARGET_TYPES(models.IntegerChoices):
    '''
    Những loại của Target
    '''
    DIRECTION = 0, _('hướng'),
    GROUP = 1, _('nhóm'),
    AREA = 2, _('địa bàn'),

# Models here.
class XFileType(models.Model):
    '''
    Biểu diễn loại (type) hồ sơ
    '''
    name = models.CharField(max_length=120)
    example_content = models.TextField() # nội dung mẫu

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.username.lower()
        return super(User, self).save(*args, **kwargs)

class Target(models.Model):
    '''
    Biểu diễn hướng - nhóm - địa bàn
    '''
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    type = models.PositiveIntegerField(choices=TARGET_TYPES.choices)

    def __str__(self):
        return f'{self.get_type_display()} {self.name}'

class XFile(models.Model):
    '''
    Biểu diễn XFile
    '''
    # Nội dung bìa
    code = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = FSMIntegerField(
        choices = STATUS.choices,
        default = STATUS.INIT,
        protected = True
    )
    date_created = models.DateField(default=timezone.now)
    type = models.ForeignKey(XFileType, on_delete=models.CASCADE)
    targets = models.ManyToManyField(Target)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    # Nội dung ẩn
    content = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=0)
    
    # Phân quyền
    editors = models.ManyToManyField(User, related_name='xfiles_can_edit')
    checkers = models.ManyToManyField(User, related_name='xfiles_can_check')
    approvers = models.ManyToManyField(User, related_name='xfiles_can_approve')
    
    def __str__(self):
        return f'hồ sơ {self.code} (ver {self.version})'

    # Chức năng riêng
    def get_xfile_content(self):
        '''
        Trả lại JSON dict thể hiện tất cả nội dung của XFile theo cấu trúc
        '''
        content = {}
        general_content = ['code', 'description', 'targets', 'department']
        for field in general_content:
            record = {}
            value = getattr(self, field)
            if type(value) == str:
                record['type'] = 'string'
            elif field == 'targets':
                record['type'] = 'target'
                value = list(value.all())
            elif field == 'department':
                record['type'] = 'department'
            record['value'] = value
            content[field] = record
        
        secret_content = decode(self.content, key=None)
        secret_content = json.loads(secret_content)
        for field, record in secret_content.items():
            if record.get('type') == 'datetime':
                try:
                    record['value'] = datetime.strptime(record['value'], '%b %d %Y').date()
                except:
                    record['value'] = date(1,1,1)

        return content | secret_content

    def get_xfile_by_version(self, version):
        '''
        Áp dụng thay đổi lần lượt, trả lại phiên bản XFile object có version tương ứng
        '''
        xfile = deepcopy(self)
        cur_version = xfile.version
        # Nếu đúng version trả về luôn
        if cur_version == version:
            return xfile
        # Nếu khác version thì áp dụng phiên bản mới (forward) 
        # hoặc lùi lại phiên bản cũ (backward)
        if cur_version < version:
            forward = 1
        else: forward = -1
        for v in range(cur_version, version, forward):
            try:
                if forward == 1:
                    change = xfile.changes.get(version = v+1)
                    change.apply_to_xfile()
                else:
                    change = xfile.changes.get(version = v)
                    change.apply_to_xfile(backward=True)
            except:
                # Nếu không tồn tại phiên bản tương ứng -> None
                return None
        return xfile

    def get_change_content(self, new_content):
        '''
        So sánh với JSON dict, trả lại JSON dict thể hiện thay đổi theo cấu trúc
        Nội dung của 2 file phải cùng dạng
        '''
        old_content = self.get_xfile_content()

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

    # Permisions control
    def can_view(self, user=None):
        if not user:
            return False
        if user in list(self.editors.all()):
            return True
        if user in list(self.checkers.all()) and self.status != STATUS.INIT:
            return True
        if user in list(self.approvers.all()) and self.status not in [STATUS.INIT, STATUS.CHECKING]:
            return True
        if user in list(User.objects.filter(info__department__alias='giamdoc')) and self.status == STATUS.DONE:
            return True
        return False

    def can_edit(self, user=None):
        if not user:
            return False
        if user in list(self.editors.all()):
            return True
        return False

    def can_check(self, user=None):
        if not user:
            return False
        if user in list(self.checkers.all()):
            return True
        return False

    def can_approve(self, user=None):
        if not user:
            return False
        if user in list(self.approvers.all()):
            return True
        return False

    # Finite-state machine
    @transition(
        field=status,
        source= STATUS.EDITING,
        target= STATUS.CHECKING,
        permission=can_edit
    )
    def submit_change(self, by=None):
        '''
        Notify checkers, save XFileChange.editor, XFileChange.date_edited
        '''
        xfilechange = self.changes.get(version = self.version)
        xfilechange.editor = by
        xfilechange.date_edited = timezone.now()
        xfilechange.save()
        notify(actor=by, target=self, verb=VERB.SEND.label, notify_to=list(self.checkers.all()))

    @transition(
        field=status,
        source= STATUS.CHECKING,
        target= STATUS.APPROVING,
        permission=can_check
    )
    def check_change(self, by=None):
        '''
        Notify approvers, save XFileChange.checker, XFileChange.date_checked
        '''
        xfilechange = self.changes.get(version = self.version)
        xfilechange.checker = by
        xfilechange.date_checked = timezone.now()
        xfilechange.save()
        notify(actor=by, target=self, verb=VERB.CHECK.label, notify_to=list(self.approvers.all()))

    @transition(
        field=status,
        source= STATUS.APPROVING,
        target= STATUS.DONE,
        permission=can_approve
    )
    def approve_change(self, by=None):
        '''
        Notify giamdoc, save XFileChange.approver, XFileChange.date_approved
        '''
        xfilechange = self.changes.get(version = self.version)
        xfilechange.approver = by
        xfilechange.date_approved = timezone.now()
        xfilechange.save()
        notify(
            actor=by, 
            target=self, 
            verb=VERB.APPROVE.label, 
            notify_to=list(User.objects.filter(info__department__alias='giamdoc'))
        )

    @transition(
        field=status,
        source= [STATUS.INIT, STATUS.DONE],
        target= STATUS.EDITING,
        permission=can_edit
    )
    def create_change(self, change_name, by=None):
        '''
        Notify editors, create new XFileChange, XFileChange.date_created,
        Apply change to XFile
        '''
        new_change = self.changes.create(name = change_name)
        new_change.date_created = timezone.now()
        new_change.apply_to_xfile()
        new_change.save()
        notify(actor=by, target=self, verb=VERB.CHANGE.label, notify_to=list(self.editors.all()))

    @transition(
        field=status,
        source= STATUS.CHECKING,
        target= STATUS.EDITING,
        permission=can_check
    )
    def reject_check(self, by=None):
        '''
        Notify editors
        '''
        notify(actor=by, target=self, verb=VERB.REJECT_CHECK.label, notify_to=list(self.editors.all()))

    @transition(
        field=status,
        source= STATUS.APPROVING,
        target= STATUS.CHECKING,
        permission=can_approve
    )
    def reject_approve(self, by=None):
        '''
        Notify checkers
        '''
        notify(actor=by, target=self, verb=VERB.REJECT_APPROVE.label, notify_to=list(self.checkers.all()))

    @transition(
        field=status,
        source= STATUS.EDITING,
        # target= STATUS.DONE,
        target= GET_STATE(
            lambda self, **kwargs: STATUS.INIT if self.version == 0 else STATUS.DONE,
            states=[STATUS.DONE, STATUS.INIT]
        ),
        permission=can_edit
    )
    def cancel_change(self, by=None):
        '''
        Notify editors, reverse change from XFile, delete XFileChange
        '''
        xfilechange = self.changes.get(version = self.version)
        xfilechange.apply_to_xfile(backward = True)
        xfilechange.delete()
        notify(actor=by, target=self, verb=VERB.CANCLE_CHANGE.label, notify_to=list(self.editors.all()))

class XFileChange(models.Model):
    '''
    Biểu diễn thay đổi của XFile
    '''
    # Nội dung được tự động tạo
    version = models.PositiveIntegerField(default=None, null=True, blank=True)
    date_created = models.DateField(default=timezone.now)
    date_edited = models.DateField(blank=True, null=True)
    date_checked = models.DateField(blank=True, null=True)
    date_approved = models.DateField(blank=True, null=True)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes_edited', null=True)
    checker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes_checked', null=True)
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes_approved', null=True)
    file = models.ForeignKey(XFile, on_delete=models.CASCADE, related_name='changes')

    # Nội dung được User chỉnh sửa
    name = models.CharField(max_length=120)
    content = models.TextField(blank=True)
    comments = GenericRelation('Comment')

    def __str__(self):
        return f'thay đổi {self.version} của {str(self.file)}'

    # Default version = xfile.version + 1
    def save(self, *args, **kwargs):
        if self.version is None:
            self.version = self.file.version + 1
        super().save(*args, **kwargs)

    # Chức năng riêng
    def apply_to_xfile(self, backward=False):
        '''
        Áp dụng thay đổi vào XFile
        '''
        xfile = self.file
        general_content = ['code', 'description', 'targets', 'department']
        secret_content = json.loads(xfile.content)
        xfile.version = self.version - backward
        try:
            change = json.loads(self.content)
        except:
            # Nếu change.content = '' -> giữ nguyên -> thoát
            return
        for field, record in change.items():
            # Nếu không có record -> lỗi -> bỏ qua và tiếp tục
            if record == None:
                continue
            type = record['type']
            if not backward:
                value = record['new']
            else:
                value = record['old']
            # Nếu thay đổi nằm trong general_content -> lưu vào XFile
            if field in general_content:
                if type == 'string':
                    setattr(xfile, field, value)
                if type == 'target':
                    targets = getattr(xfile, field)
                    targets.set(Target.objects.filter(id__in = value))
                if type == 'department':
                    setattr(xfile, field, Department.objects.get(id = value))
            # Nếu thay đổi trong secret_content -> lưu vào secret_content
            if field in secret_content.keys():
                secret_content[field] = record

        xfile.content = json.dumps(secret_content)

    def update(self, dict_content):
        '''
        Chuyển đổi JSON dict thành JSON string và lưu vào XFileChange.content
        '''
        for field, record in dict_content.items():
            # Nếu không có record -> lỗi -> bỏ qua
            if record == None:
                continue
            type = record['type']
            old_value = record['old']
            new_value = record['new']
            # Nếu dữ liệu thuộc class đặc biệt -> thay đổi để serialize ra JSON string
            if type == 'target':
                record['old'] = [target.id for target in old_value]
                record['new'] = [target.id for target in new_value]
            if type == 'department':
                record['old'] = old_value.id
                record['new'] = new_value.id
            if type == 'datetime':
                record['old'] = date.strftime(old_value, '%b %d %Y')
                record['new'] = date.strftime(new_value, '%b %d %Y')

        self.content = json.dumps(dict_content)
        self.save()
    
class Comment(models.Model):
    '''
    Biểu diễn nhận xét của User
    '''
    # Nội dung được tự động tạo
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # Nội dung được User chỉnh sửa
    body = models.TextField()

    def __str__(self):
        return f'Comment by {self.author}'

class AttackLog(models.Model):
    '''
    Biểu diễn bảng IV: theo dõi quá trình theo dõi/tấn công
    '''
    timestamp = models.DateField()
    name = models.TextField(blank=True)
    content = models.TextField(blank=True)
    attacker = models.TextField(blank=True)

    file = models.ForeignKey(XFile, on_delete=models.CASCADE, related_name='attack_logs')

    def __str__(self):
        return f'quá trình {self.name}'