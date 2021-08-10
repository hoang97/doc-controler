from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.forms.models import model_to_dict
from hsmt.utils import notify, VERB
import hsmt.models as db
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
LIST_GROUPS=(
    "Trợ lí",
    "Trưởng phòng",
    "Giám đốc"
)
LIST_XFILE_TYPES =(
    "Trang mạng",
    'Tổ chức',
    'Đối tượng'
)
def JsonResponseError(msg):
    ''' Trả về ({"status":-1,"msg":msg}) '''
    return JsonResponse({"status":-1,"msg":msg})
def JsonResponseSuccess(data):
    ''' Trả về ({"status":0,"data":data}) '''
    return JsonResponse({"status":0,"data":data})



# Create your views here.
class XFileCreateView(CreateView):
    template_name = 'hsmt/create.html'
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
    template_name = 'hsmt/list.html'
    model = XFile
    context_object_name = 'xfile_list'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Danh mục các hồ sơ mục tiêu'
        return context

class XFileDetailView(DetailView):
    template_name = 'hsmt/detail.html'
    model = XFile
    context_object_name = 'xfile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chi tiết về hồ sơ mục tiêu'
        return context

class XFileDeleteView(DeleteView):
    template_name = 'hsmt/base.html'
    model = XFile
    success_url = reverse_lazy('hsmt-list')

class XFileChangeDetailView(DetailView):
    template_name = 'hsmt/change_detail.html'
    model = XFileChange
    context_object_name = 'change'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chi tiết về thay đổi'
        return context

class XFileTypeListView(ListView):
    template_name = 'hsmt/type_list.html'
    model = XFileType
    context_object_name = 'xfiletype_list'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Danh mục các loại hồ sơ'
        return context

class XFileTypeCreateView(CreateView):
    template_name = 'hsmt/type_create.html'
    model = XFileType
    fields = ['name','example_content']
    success_url = reverse_lazy('hsmt-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tạo loại hồ sơ mới'
        return context

class XFileTypeDetailView(DetailView):
    template_name = 'hsmt/type_detail.html'
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



#======================TARGET_TYPES VIEWS========================    
@login_required
def target_type_list(request):
    title='Hướng - Nhóm - Địa bàn'
    context={
    'breadcrumb':title,
    'h1header':title
    }
    # context['user_role']=get_user_role(request.user)
    context['user_layout']=request.user
    return render(request, 'hsmt/target-type-list.html',context)

@login_required
def get_all_target_types(request):
    data = list(db.Target.objects.all().values())
    return JsonResponseSuccess(data)

#trả về danh sách theo hướng, nhóm địa bàn    
@login_required
def get_target_type_by_type(request):
    targetType=request.GET.get('targetType','')
    data=[]
    if targetType:
        for TARGET_TYPE in db.TARGET_TYPES:
            if str(TARGET_TYPE) ==targetType:
                data=list(db.Target.objects.filter(type=TARGET_TYPE).values())
                break
    return JsonResponseSuccess(data)

#trả về danh sách hướng, nhóm, địa bàn theo id
@login_required
def get_target_type_by_id(request):
    target_type_id=request.GET.get('id','')
    if (not target_type_id):
        msg ="Failed"
        return  JsonResponseError(msg) 
    data={}
    data=db.Target.objects.filter(id=target_type_id).values()[0]

    return JsonResponseSuccess(data)

@login_required
def add_edit_target_type(request):
    """
    Thêm - Sửa target_type
    """
    try:
        targetId=request.POST['target-id']
        targetName=request.POST['target-name']
        targetType=request.POST['target-type']
        targetDesc=request.POST['target-desc']

    except:
        return JsonResponseError("Thiếu dữ liệu")
    if targetId:
        # Có ID = UPDATE
        target= db.Target.objects.get(id=targetId)
        target.name=targetName
        target.description=targetDesc
        # target.target_type=
        target.save()
    else:
        # Không ID = CREATE NEW
        newObj= db.Target.objects.create(name=targetName,description=targetDesc,type=targetType)
        newObj.save()
        return JsonResponseSuccess(model_to_dict(newObj))
    msg ='Done'
    return JsonResponseSuccess(msg)



@login_required
def delete_target_type(request):
    try:
        targetId=request.POST['target-id']
    except:
        return JsonResponseError("Thiếu dữ liệu")
    msg=''
    if targetId:
        oldObj= db.Target.objects.get(id=targetId)
        # ktra xem da duoc su dung boi Xfile nao chua
        # https://djangotricks.blogspot.com/2018/05/queryset-filters-on-many-to-many-relations.html
        if  db. XFile.objects.filter(targets__type=targetId).count() > 0:
            return JsonResponseError("Không thể xoá do đang sử dụng bởi HSMT")
        oldObj.delete()
        msg='Xoá thành công'
    return JsonResponseSuccess(msg)



def test(request):
    pwd=hash_password('2')
    print(pwd)
    return JsonResponseError('')    