from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

def get_user_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.user.id}/{filename}"

# Create your models here.
class DepartmentManager(models.Manager):
    def create_department(self, alias, password, name, **kwargs):
        department = self.model(alias=alias, name=name, **kwargs)
        department.password = make_password(password)
        department.save(using=self._db)
        return department

class Department(models.Model):
    '''
    Biểu diễn các phòng trong cơ quan
    '''
    name = models.TextField()
    alias = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=150)
    objects = DepartmentManager()

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

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    # Thông tin chi tiết về User
    first_name = models.CharField(max_length=150)
    image = models.ImageField(default="default.jpg", upload_to=get_user_dir_path)
    address = models.TextField(blank=True)
    skill = models.TextField(blank=True)
    phone_number = models.TextField(blank=True)
    self_introduction = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    layout_config = models.TextField(blank=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Tài khoản {self.username}"