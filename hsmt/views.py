from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from hsmt.utils import notify, VERB
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django_fsm import can_proceed, has_transition_perm
from .models import (
    XFile, 
    XFileChange, 
    Comment,
    XFileType,
    STATUS,
)
# Create your views here.
class XFileCreateView(CreateView):
    template_name = 'hsmt/old/create.html'
    model = XFile
    fields = ['code', 'description','type', 'targets', 'editors', 'checkers', 'approvers']
    success_url = reverse_lazy('hsmt-list')

    def form_valid(self, form):
        xfile = form.instance
        xfile.department = self.request.user.info.department
        xfile.content = xfile.type.example_content
        httpresponse = super().form_valid(form)
        notify(actor=self.request.user, target=xfile, verb=VERB.CREATE.label, notify_to=list(xfile.editors.all()))
        return httpresponse

class XFileListView(ListView):
    template_name = 'hsmt/old/list.html'
    model = XFile
    context_object_name = 'xfile_list'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Danh mục các hồ sơ mục tiêu'
        return context

class XFileDetailView(DetailView):
    template_name = 'hsmt/old/detail.html'
    model = XFile
    context_object_name = 'xfile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chi tiết về hồ sơ mục tiêu'
        return context

class XFileDeleteView(DeleteView):
    template_name = 'hsmt/old/base.html'
    model = XFile
    success_url = reverse_lazy('hsmt-list')

class XFileChangeDetailView(DetailView):
    template_name = 'hsmt/old/change_detail.html'
    model = XFileChange
    context_object_name = 'change'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chi tiết về thay đổi'
        return context

class XFileTypeListView(ListView):
    template_name = 'hsmt/old/type_list.html'
    model = XFileType
    context_object_name = 'xfiletype_list'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Danh mục các loại hồ sơ'
        return context

class XFileTypeCreateView(CreateView):
    template_name = 'hsmt/old/type_create.html'
    model = XFileType
    fields = ['name','example_content']
    success_url = reverse_lazy('hsmt-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tạo loại hồ sơ mới'
        return context

class XFileTypeDetailView(DetailView):
    template_name = 'hsmt/old/type_detail.html'
    model = XFileType
    context_object_name = 'xfiletype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chi tiết về loại hồ sơ'
        return context

@login_required
def get_permission_user_xfile(request, pk):
    xfile = get_object_or_404(XFile, id=pk)
    user = request.user
    data = {
        'view': xfile.can_view(user),
        'createChange': has_transition_perm(xfile.create_change, user),
        'edit': has_transition_perm(xfile.cancel_change, user),
        'cancel': has_transition_perm(xfile.cancel_change, user),
        'submit': has_transition_perm(xfile.submit_change, user),
        'check': has_transition_perm(xfile.check_change, user),
        'rejectCheck': has_transition_perm(xfile.reject_check, user),
        'approve': has_transition_perm(xfile.approve_change, user),
        'rejectApprove': has_transition_perm(xfile.reject_approve, user),
    }
    return JsonResponse(data)

@login_required
def create_change_xfile(request, pk):
    if request.method == 'POST':
        xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
        user = request.user
        if has_transition_perm(xfile.create_change, user):
            change_name = request.POST.get("change_name","")
            if not change_name:
                return JsonResponse({'msg': 'change_name cant be empty'})
            xfile.create_change(change_name, by=user)
            xfile.save()
            notify(actor=user, target=xfile, verb=VERB.CHANGE.label, notify_to=list(xfile.editors.all()))
            return redirect('hsmt-detail', pk=pk)
        else:
            return JsonResponse({'msg': 'permission denie'})

@login_required
def cancel_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
    user = request.user
    if has_transition_perm(xfile.cancel_change, user):
        xfile.cancel_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.CANCLE_CHANGE.label, notify_to=list(xfile.editors.all()))
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})

@login_required
def submit_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)
    user = request.user
    if has_transition_perm(xfile.submit_change, user):
        xfile.submit_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.SEND.label, notify_to=list(xfile.checkers.all()))
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})

@login_required
def check_change_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('approvers'), id=pk)
    user = request.user
    if has_transition_perm(xfile.check_change, user):
        xfile.check_change(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.CHECK.label, notify_to=list(xfile.approvers.all()))
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})

@login_required
def reject_check_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('editors'), id=pk)
    user = request.user
    if has_transition_perm(xfile.reject_check, user):
        xfile.reject_check(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.REJECT_CHECK.label, notify_to=list(xfile.editors.all()))
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})

@login_required
def approve_change_xfile(request, pk):
    xfile = get_object_or_404(XFile, id=pk)
    user = request.user
    if has_transition_perm(xfile.approve_change, user):
        xfile.approve_change(by=user)
        xfile.save()
        notify(
            actor=user, target=xfile, verb=VERB.APPROVE.label, 
            notify_to=list(User.objects.filter(info__department__alias='giamdoc'))
        )
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})

@login_required
def reject_approve_xfile(request, pk):
    xfile = get_object_or_404(XFile.objects.prefetch_related('checkers'), id=pk)
    user = request.user
    if has_transition_perm(xfile.reject_approve, user):
        xfile.reject_approve(by=user)
        xfile.save()
        notify(actor=user, target=xfile, verb=VERB.REJECT_APPROVE.label, notify_to=list(xfile.checkers.all()))
        return redirect('hsmt-detail', pk=pk)
    else:
        return JsonResponse({'msg': 'permission denie'})