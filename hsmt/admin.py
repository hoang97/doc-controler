from django.contrib import admin
from .models import (
    XFile, 
    XFileChange, 
    Comment,
    XFileType,
    Target,
    AttackLog
)

# Register your models here.
admin.site.register(XFile)
admin.site.register(XFileChange)
admin.site.register(Comment)
admin.site.register(XFileType)
admin.site.register(Target)
admin.site.register(AttackLog)