from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils import timezone
from django.forms.models import model_to_dict
from notifications.utils import notify, VERB
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
    Target,
    TARGET_TYPES
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

def _get_queryset(klass):
    """
    This is copy of _get_queryset in django.shortcuts
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass

def get_object_or_none(klass, *args, **kwargs):
    """
    This is copy of django.shortcuts.get_object_or_404
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_none() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

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
            return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
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
        return redirect(reverse('edit-detail')+f'?id={pk}')
    else:
        return JsonResponse({'msg': 'permission denie'})

#======================XFILEs VIEWS========================    

@login_required
def hsmt_list(request):
    title='Danh sách HSMT'
    context={
    'breadcrumb':title,
    'h1header':title,
    }
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user
    return render(request, 'hsmt/hsmt-list.html',context)

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
    isChecker=xfile.can_check(request.user)
    # if db.Xfile.objects.filter(id=xfileId).count() >0:
    #     xfile=db.Xfile.objects.get(id=xfileId)
    #     if not xfile.original:
    #         if xfile.duplicate:
    #             originalXfileId=xfile.duplicate
    #         elif xfile.history:
    #             originalXfileId=xfile.history
    #     # List[Tuple[int, str]]
    #     for XFILE_TYPE in db.XFILE_TYPES:
    #         if xfile.xfile_type==XFILE_TYPE:
    #             title=title+' - '+XFILE_TYPE.label
    #             xfile_type=str(XFILE_TYPE)
    #             break
    #     #Quản lý quyền 
    #     if db.Xfile_role.objects.filter(role=db.XFILE_ROLES.CHECKER, xfile=xfile,user=request.user).count()  >0:
    #         isChecker=True
    #     if xfile.history:
    #         context['historyId']=xfile.history
        
    context['xfile_type'] = str(xfile.type.id)
    context['xfileId']=xfileId
    context['xfile_status']=xfile.get_status_display()
    context['originalXfileId']=originalXfileId
    context['breadcrumb']=title
    context['h1header']=title

    #Quản lý quyền 
    if isChecker == True:
        context['user_role']='05'
    else:
        context['user_role'] = str(request.user.info.position.id)
    context['user_layout']=request.user
    return render(request, 'hsmt/hsmt-detail.html',context)

@login_required
def get_xfile_by_id(request):
    # API dùng để lấy thông tin xfile
    xfileId = request.GET.get('id', -1)
    onlyXfileCover=request.GET.get('onlyXfileCover','')
    #Getiing Xfile
    try:
        xfile = XFile.objects\
            .select_related('creator')\
            .select_related('type')\
            .prefetch_related('targets')\
            .get(id=xfileId)
    except:
        return JsonResponseError('HSMT không tồn tại hoặc đã bị xoá')

    # originalXfileId=xfile.id
    # if not xfile.original:
    #     if xfile.duplicate:
    #         originalXfileId=xfile.duplicate
    #     elif xfile.history:
    #         originalXfileId=xfile.history
    #Check Authorized
    isGiamdoc=False
    if not xfile.can_view(request.user):
        return JsonResponseError("Không đủ thẩm quyền")

    values=[]
    isDecrypted=True
    msg='Lấy dữ liệu chi tiết HSMT thành công'
    # pwd=''
    # if isGiamdoc:
    #     pwd=request.session.get(xfile.department.alias,'')
    # else:
    #     pwd=request.session.get('dp','')
    # if not compare_passwords(pwd,xfile.department.password):
    #     msg='Mật khẩu '+xfile.department.name+' đã thay đổi hoặc chưa thiết lập mật khẩu'
    #     pwd=False
    # else:
    #     isDecrypted=True
    #     if not onlyXfileCover:
    #         if xfile.value:
    #             old_value_decrypted={}
    #             if xfile.history:
    #                 historyXfile=db.Xfile.objects.filter(id=xfile.history).values('value').first()
    #                 if historyXfile:
    #                     old_value_decrypted=historyXfile['value']
    #             elif xfile.duplicate:
    #                 dupXfile=db.Xfile.objects.filter(id=xfile.duplicate).values('value').first()
    #                 if dupXfile:
    #                     old_value_decrypted=dupXfile['value']
    #             value_decrypted=''
    #             try:
    #                 raw_value=AESdecrypt(xfile.value,pwd)
    #                 value_decrypted=json.loads(raw_value)
    #                 if old_value_decrypted:
    #                     try:
    #                         old_value_decrypted=json.loads(AESdecrypt(old_value_decrypted,pwd))
    #                     except:
    #                         print("Khoong giai  mã được old_value_decrypted")
    #             except:
    #                 msg="Không thể giải mã HSMT"
    #             if not (type(value_decrypted) is dict):
    #                 #Nếu có giá trị --> không decrypt ra Dictionary --> mậT khẩu sai
    #                 isDecrypted=False
    #             if not (type(old_value_decrypted) is dict):
    #                 old_value_decrypted={}

    #             if isDecrypted and len(value_decrypted) >0:
    #                 for key in value_decrypted.keys(): 
    #                         # [alias, val]
    #                         tmp=[key,value_decrypted[key],False]

    #                         if key in old_value_decrypted:
    #                             print('ori='+ value_decrypted[key])
    #                             print('dup='+ old_value_decrypted[key])
    #                             if value_decrypted[key] != old_value_decrypted[key]:
    #                                 tmp[2]=True
    #                         values.append(tmp)
    targets = xfile.targets.all()
    data={
        # 'xfile':model_to_dict(xfile),
        'id':xfile.id,
        'name': 'Miêu tả về hồ sơ', # xfile.name,
        'code':xfile.code,
        'description':xfile.description,
        'duplicate': 'need fix', # xfile.duplicate,
        'original': 'need fix', # xfile.original,
        'history': 'need fix', # xfile.history,
        'date_created':xfile.date_created,
        'version': xfile.version,
        'edit_note': 'need fix', # xfile.edit_note,
        "status":xfile.status,
        'values': 'need fix', # values,
        'isDecrypted': isDecrypted,
        "xfile_type": xfile.type.id,
        'department':xfile.department.name,
        'targetTypes':{
            'target-direction': list(targets.filter(type=TARGET_TYPES.DIRECTION).values()),
            'target-group': list(targets.filter(type=TARGET_TYPES.GROUP).values()),
            'target-area': list(targets.filter(type=TARGET_TYPES.AREA).values())
        }, 
        'user': model_to_dict(xfile.creator),
        'msg':msg
    }    
    return JsonResponseSuccess(data)

@login_required
def get_xfile_update(request):
    '''Lấy ra danh sách XFileChange của XFile'''
    xfileId=request.GET.get('xfileId', -1)
    xfile= get_object_or_none(XFile, id=xfileId)
    if not xfile:
        return JsonResponseError('HSMT không tồn tại!')
    data= list(xfile.changes.values())
    return JsonResponseSuccess(data)

@login_required
def get_xfile_user_role(request):
    ''' filter= None=ALL, 1: Creator, filter=2: edtior, filter=3, checkers, '''
    xfileId=request.POST.get('xfileId', -1)
    # fetchAllUsers=request.POST.get('fetchAllUsers','')
    try:
        xfile = XFile.objects\
            .select_related('creator')\
            .prefetch_related('editors')\
            .prefetch_related('checkers')\
            .prefetch_related('approvers')\
            .get(id=xfileId)
    except:
        return JsonResponseError('HSMT không tồn tại - Không tìm được Quyền')
    data={
        'creator': model_to_dict(xfile.creator, fields=['username', 'first_name']),
        'editors': list(xfile.editors.values('username', 'first_name')),
        'checkers': list(xfile.checkers.values('username', 'first_name')),
        'approvers': list(xfile.approvers.values('username', 'first_name')),
    }

    return JsonResponseSuccess(data)

@login_required
def get_perm_user_xfile(request):
    xfileId = request.POST.get('xfileId', -1)
    try:
        xfile = XFile.objects.get(id=xfileId)
    except:
        return JsonResponseError('HSMT không tồn tại hoặc đã bị xóa')
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
    return JsonResponseSuccess(data)

@login_required
def get_xfiles(request):
    isGiamdoc=False
    if request.user.info.position.id == 1:
        ''' Nếu là trợ lý thì có quyền xem hsmt mình có quyền chỉnh sửa hoặc kiểm tra'''
        xfileuseredit = request.user.xfiles_can_edit.all().prefetch_related('editors').prefetch_related('checkers')
        xfileusercheck  = request.user.xfiles_can_check.all().prefetch_related('editors').prefetch_related('checkers')
        xfiles = xfileuseredit.union(xfileusercheck)
    elif request.user.info.position.id == 2:
        '''Nếu là trưởng phòng có quyền xem tất cả hsmt của phòng mình'''
        xfiles=XFile.objects.filter(department=request.user.info.department).prefetch_related('editors').prefetch_related('checkers')
    elif request.user.info.position.id == 3:
        '''giám đốc có quyền xem tất cả hsmt'''
        xfiles=XFile.objects.filter().prefetch_related('editors').prefetch_related('checkers')
        isGiamdoc=True
    else:
        return JsonResponseError("Không đủ thẩm quyền")
    data=[]
    for xfile in xfiles:
        if xfile is None:
            continue
        tmp={
            # 'xfile':model_to_dict(xfile),
            'id':xfile.id,
            'code':xfile.code,
            'date_created':xfile.date_created,
            # 'date_modified':xfile.date_modified,
            # 'edit_note':xfile.edit_note,
            "status":xfile.status,
            "xfile_type":xfile.type.id,
            "department":xfile.department.name,
            'editors':[],
            'checkers':[],
            'ct':isGiamdoc,
        }    
        checkers = xfile.checkers.all()
        editors = xfile.editors.all()
        for checker in checkers:
            tmp['checkers'].append({"id":checker.id,"first_name":checker.first_name,"username":checker.username,"is_active":checker.is_active}) 
        for editor in editors:
            tmp['editors'].append({"id":editor.id,"first_name":editor.first_name,"username":editor.username,"is_active":editor.is_active}) 
        data.append(tmp)

    return JsonResponseSuccess(data)

@login_required
def hsmt_filter(request):
    title='Danh sách HSMT'
    context={
    'breadcrumb':title,
    'h1header':title,
    }
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user
    xfileStatusId = request.GET.get('status','')
    if not xfileStatusId:
        msg="khong co du lieu"
        return JsonResponseError(msg)
    context['xfileStatusId']=xfileStatusId
    return render(request, 'hsmt/hsmt-filter.html',context)

#======================TARGET_TYPES VIEWS========================    
@login_required
def target_type_list(request):
    title='Hướng - Nhóm - Địa bàn'
    context={
    'breadcrumb':title,
    'h1header':title
    }
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user
    return render(request, 'hsmt/target-type-list.html',context)

@login_required
def get_all_target_types(request):
    data = list(Target.objects.all().values())
    return JsonResponseSuccess(data)

#trả về danh sách theo hướng, nhóm địa bàn    
@login_required
def get_target_type_by_type(request):
    targetType=request.GET.get('targetType','')
    data=[]
    if targetType:
        for TARGET_TYPE in TARGET_TYPES:
            if str(TARGET_TYPE) ==targetType:
                data=list(Target.objects.filter(type=TARGET_TYPE).values())
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
    data=Target.objects.filter(id=target_type_id).values()[0]

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
        target= Target.objects.get(id=targetId)
        target.name=targetName
        target.description=targetDesc
        # target.target_type=
        target.save()
    else:
        # Không ID = CREATE NEW
        newObj= Target.objects.create(name=targetName,description=targetDesc,type=targetType)
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
        oldObj= Target.objects.get(id=targetId)
        # ktra xem da duoc su dung boi Xfile nao chua
        # https://djangotricks.blogspot.com/2018/05/queryset-filters-on-many-to-many-relations.html
        if  XFile.objects.filter(targets__type=targetId).count() > 0:
            return JsonResponseError("Không thể xoá do đang sử dụng bởi HSMT")
        oldObj.delete()
        msg='Xoá thành công'
    return JsonResponseSuccess(msg)
