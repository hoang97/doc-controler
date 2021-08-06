from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class DETAIL_URL(models.TextChoices):
    USER = 'user', 'user-profile'
    XFILE = 'x file', 'hsmt-detail'

# Create your models here.
class Log(models.Model):
    '''
    Biểu diễn 1 sự kiện của hệ thống
    - vd: 
        - trưởng phòng A (actor) đã phê duyệt (verb) hồ sơ B (target) lúc 11h30 22/1/2021 (timestamp)
        - giám đốc (actor) đã tạo mới (verb) tài khoản C (target) lúc 20h21 20/1/2021 (timestamp)
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

    def get_target_url(self):
        '''
        Trả lại url đến trang web chi tiết về target
        '''
        return reverse(DETAIL_URL(self.target_ct.name).label, args=[self.target_id])

class Notification(models.Model):
    '''
    Thông tin về thông báo của người dùng
    '''
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)