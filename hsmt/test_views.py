from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from hsmt.models import *
from notifications.utils import notify, VERB

# XFile views

@login_required
def hsmt_list_view(request):
    title='Danh sách HSMT'
    context={
        'breadcrumb':title,
        'h1header':title,
        'xfile_types': XFileType.objects.all(),
        'users': User.objects.filter(info__department=request.user.info.department).select_related('info__position'),
        'targets': Target.objects.all()
    }
    return render(request, 'hsmt/hsmt-list.html',context)

@login_required
def target_list_view(request):
    title='Danh sách Hướng - Nhóm - Địa Bàn'
    context={
        'breadcrumb':title,
        'h1header':title,
        'targets': TARGET_TYPES.choices
    }
    return render(request, 'hsmt/target-type-list.html',context)