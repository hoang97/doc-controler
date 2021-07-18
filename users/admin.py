from django.contrib import admin
from .models import (
    UserInfor, 
    Department, 
)

# Register your models here.
admin.site.register(UserInfor)
admin.site.register(Department)