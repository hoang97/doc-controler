from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _

class VERB(models.TextChoices):
    '''
    Những hành động của User
    '''
    CHANGE = 'change', _('sửa đổi')
    SEND = 'send', _('gửi kiểm định')
    CHECK = 'check', _('kiểm định')
    APPROVE = 'approve', _('phê duyệt')
    CREATE = 'create', _('tạo mới')
    REJECT_CHECK = 'reject check', _('yêu cầu sửa lại')
    REJECT_APPROVE = 'reject approve', _('yêu cầu kiểm định lại')
    CANCLE_CHANGE = 'cancle change', _('hủy bỏ sửa đổi')

# Create your models here.
class Log(models.Model):
    '''
    Biểu diễn 1 sự kiện của hệ thống
    vd: 
    trưởng phòng A (actor) đã phê duyệt (verb) hồ sơ B (target) lúc 11h30 22/1/2021 (timestamp)
    giám đốc (actor) đã tạo mới (verb) tài khoản C (target) lúc 20h21 20/1/2021 (timestamp)
    '''
    timestamp = models.DateTimeField(default=timezone.now)
    # actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # target = models.ForeignKey(XFile, on_delete=models.CASCADE)
    actor_ct = ForeignKey(ContentType, on_delete=models.CASCADE, related_name='log_actors')
    actor_id = models.PositiveIntegerField()
    target_ct = ForeignKey(ContentType, on_delete=models.CASCADE, related_name='log_targets')
    target_id = models.PositiveIntegerField()

    actor = GenericForeignKey('actor_ct','actor_id')
    target = GenericForeignKey('target_ct','target_id')
    verb = models.TextField()
    notify_to = models.ManyToManyField(User, through='Notification')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{str(self.actor)} đã {self.verb} {str(self.target)}'

class Notification(models.Model):
    '''
    Thông tin về thông báo của người dùng
    '''
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)