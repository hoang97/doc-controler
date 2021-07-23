from django.contrib import admin
from .models import (
    UserInfor, 
    Department, 
    Position, 
)

# Register your models here.
admin.site.register(UserInfor)
admin.site.register(Department)
admin.site.register(Position)