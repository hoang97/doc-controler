from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Department, 
    Position, 
    User
)

class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'first_name', 'id')
    ordering = ('-date_joined', )
    list_display = ('username', 'id', 'first_name', 'is_active', 'is_staff')
    list_filter = ('username', 'first_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal', {'fields': ('first_name', 'image', 'address', 'skill', 'phone_number', 'self_introduction', 'email', 'layout_config')}),
        ('Company info', {'fields': ('department', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Position)