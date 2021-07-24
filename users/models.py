from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def get_user_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.user.id}/{filename}"

# Create your models here.
class Department(models.Model):
    '''
    Biểu diễn các phòng trong cơ quan
    '''
    name = models.TextField()
    alias = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    '''
    Biểu diễn chức vụ trong tổ chức
    '''
    name = models.TextField()
    alias = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserInfor(models.Model):
    '''
    Thông tin thêm về User
    '''
    # Nội dung được tự động tạo
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')

    # Thông tin thêm về User
    image = models.ImageField(default="default.jpg", upload_to=get_user_dir_path)
    address = models.TextField(blank=True)
    skill = models.TextField(blank=True)
    phone_number = models.TextField(blank=True)
    self_introduction = models.TextField(blank=True)
    layout_config = models.TextField(blank=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Tài khoản {self.user.username}"
