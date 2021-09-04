from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from django.http import HttpResponseForbidden

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
        'users': User.objects.filter(department=request.user.department).select_related('position'),
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

@login_required
def hsmt_edit_detail(request):
    xfileId = request.GET.get('id',-1)
    title='Chỉnh sửa HSMT'
    context={ }
    # xfile_type='1'
    originalXfileId=xfileId
    xfile = get_object_or_404(XFile, id=xfileId)
    if not xfile.can_view(request.user):
        return HttpResponseForbidden()

    title += ' - '+ xfile.type.name
        
    context['xfile_type'] = str(xfile.type.id)
    context['xfileId']=xfileId
    context['xfile_status']=xfile.get_status_display()
    context['originalXfileId']=originalXfileId
    context['breadcrumb']=title
    context['h1header']=title
    context['user_layout']=request.user
    return render(request, 'hsmt/hsmt-detail.html',context)