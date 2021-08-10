from django.urls.base import reverse
from users.models import Department, Position, UserInfor
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
import users.models as db

def display_form_error(request, errors):
    for obj, err in errors.items():
        msg = f"{obj}: {err[0]}"
        messages.error(request, msg)

# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': 'Blog Controller Login'
    }
    
    def form_valid(self, form):
        messages.success(self.request, 'Đăng nhập thành công!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Tài khoản hoặc mật khẩu không đúng!!!')
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = 'user-login'
    extra_context = {
        'title': 'Blog Controller Logout'
    }

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user-login')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'User Register'
        return context
        
    def form_valid(self, form):
        form.instance.first_name = self.request.POST.get('first_name')
        form.instance.last_name = self.request.POST.get('last_name')
        messages.success(self.request, 'Tài khoản được tạo thành công!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        display_form_error(self.request, form.errors)
        return super().form_invalid(form)

class UserProfileView(DetailView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Profile'
        return context

class UserProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/update.html'
    model = User
    fields = ['username']
    context_object_name = 'user'
    permission_denied_message = 'Không có quyền sửa đổi tài khoản này'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Update'
        return context

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    # Handle if there's a POST requets
    msg = ''
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(request, username=username, password=password )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    msg = 'Tài khoản chưa kích hoạt. Hãy liên hệ với trưởng phòng để xác nhận!'
            else:
                msg = 'Tài khoản hoặc mật khẩu không đúng'
        else:
            msg = 'Hãy nhập tài khoản và mật khẩu.'

    # Render login template by default 
    context = {
        'msg': msg,
        'h1header': 'Đăng nhập'
    }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('user-login')

def success_view(request):
    departmentNumber = request.GET.get('departmentNumber', '')
    context = {
        'h1header': 'Đăng ký thành công',
        'departmentNumber': departmentNumber
    }
    return render(request, 'users/success.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    # Handle if there's a POST requets
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password=request.POST.get('password', '')
        departmentNumber=request.POST.get('phong', '')
        fullname=request.POST.get('fullname', '')
        # Validate POST data
        if username and password and departmentNumber and fullname:
            if User.objects.filter(username=username).count() > 0:
                msg="Tên tài khoản đã tồn tại"
            elif Department.objects.filter(id=departmentNumber).count() == 0:
                msg="Không có phòng này tồn tại"
        else:
            msg="Hãy điền đầy đủ thông tin"
        # Create User if data is validated
        if msg == '':
            user = User.objects.create_user(username=username, password=password, first_name=fullname, is_active=False)
            user.info.department = Department.objects.get(id=departmentNumber)
            user.info.position = Position.objects.get(alias='tk')
            user.info.save()
            return redirect(reverse('user-success') + f'?departmentNumber={departmentNumber}')

    context = {
        'msg': msg,
        'h1header': 'Đăng ký tài khoản',
        'department_list': Department.objects.exclude(alias='giamdoc')
    }
    return render(request, 'users/register.html', context)

# API here

def JsonResponseError(msg):
    ''' Trả về ({"status":-1,"msg":msg}) '''
    return JsonResponse({"status":-1,"msg":msg})
def JsonResponseSuccess(data):
    ''' Trả về ({"status":0,"data":data}) '''
    return JsonResponse({"status":0,"data":data})

@login_required
def register_api(request):
    '''
    - Create new user (has same department as creater)
    '''
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password=request.POST.get('password', '')
        fullname=request.POST.get('fullname', '')
        # Validate POST data
        if username and password and fullname:
            if User.objects.filter(username=username).count() > 0:
                msg="Tên tài khoản đã tồn tại"
        else:
            msg="Hãy điền đầy đủ thông tin"
        # Create User if data is validated
        if msg == '':
            user = User.objects.create_user(username=username, password=password, first_name=fullname, is_active=False)
            user.info.department = request.user.info.department
            user.info.position = Position.objects.get(alias='tk')
            user.info.save()
            return JsonResponseSuccess('Tạo tài khoản thành công!')
    return JsonResponseError(msg)



# =================== CRUD USER =============

@login_required
def get_users(request):
    ''' Auto get users by his department'''
    onlyEditor=str(request.GET.get('onlyEditor',''))
    # Retrive user department
    data={
        'users':[],
        'owner_group':[group.name for group in request.user.po.all()]
    }
    queryset=db.UserInfor.objects.filter(department=request.user.Userinfo.department).select_related('user')
    
    for user_info in queryset:
        flag=False
        if  onlyEditor != '1':
            flag=True
        elif user_info.user.groups.filter(name=LIST_GROUPS[0]).count()>0:
            flag=True
        if flag==True:
            data['users'].append({
                "id":user_info.user.id,
                "first_name":user_info.user.first_name,
                "last_login":user_info.user.last_login,
                "date_joined":user_info.user.date_joined,
                "username":user_info.user.username,
                "is_active":user_info.user.is_active,
                "groups":[group.name for group in user_info.user.groups.all()]
                 })
        # data['allUsers'].append({"id":user_info.user.id,"first_name":user_info.user.first_name,"username":user_info.user.username,"is_active":user_info.user.is_active})
   
    return JsonResponseSuccess(data)

@login_required
def activate_user(request):
    if request.user.groups.filter(name=LIST_GROUPS[1]).count() == 0:
        return JsonResponseError('Không đủ thẩm quyền')
    userId=request.POST.get('userId','')
    if not userId:
        return JsonResponseError('Không đủ dữ liệu')
    userForChanged=User.objects.get(id=userId)
    if (userForChanged==request.user):
        return JsonResponseError('Không thể huỷ kích hoạt chính mình')
    if (userForChanged.user_info.department!=request.user.user_info.department):
        return JsonResponseError('Không thuộc phòng của bạn')
    userForChanged.is_active=not userForChanged.is_active
    userForChanged.save()
    
    return JsonResponseSuccess('Thành công')
def delete_user(request):
    if request.user.groups.filter(name=LIST_GROUPS[1]).count() == 0:
        return JsonResponseError('Không đủ thẩm quyền')
    userId=request.POST.get('userId','')
    if not userId:
        return JsonResponseError('Không đủ dữ liệu')
    userDelete=User.objects.get(id=userId)
    if userDelete.groups.filter(name=LIST_GROUPS[1]).count() >0:
        msg='Không thể xoá người dùng Trưởng Phòng'
        return JsonResponseError(msg)
    log_msg=request.user.first_name+" đã xoá người dùng "+userDelete.first_name +" ("+userDelete.username+")"
    userDelete.delete()
    #Ghi log
    log_action(request.user,log_msg,action_type=db.ACTION_TYPES.DELETION)
    
    return JsonResponseSuccess('Thành công')
@login_required
def profile(request):
    userName=request.GET.get('u','')
    selfProfile=False
    if (request.user.username==userName):
        selfProfile=True
    userInfo = db.User_info.objects.filter(user=User.objects.get(username=userName)).select_related('user')[0]
    originalUser=User.objects.get(username=userName)
    totalXfile=db.Xfile_role.objects.filter(user=originalUser,role=db.XFILE_ROLES.CREATOR).count()
    group_name=list(userInfo.user.groups.all())
    title='Trang cá nhân'
    context={
        'user':{
            'username':userInfo.user.username,
            'first_name':userInfo.user.first_name,
            'last_login':userInfo.user.last_login,
            'is_active':userInfo.user.is_active,
            'group_name':str(group_name[0].name),
            'totalXfile':totalXfile
        },
        'userInfo':{
            'skill':userInfo.skill,
            'address':userInfo.address,
            'phone_number':userInfo.phone_number,
            'self_introdution':userInfo.self_introdution
        },
        'user_layout':request.user,
        'breadcrumb':title,
        'h1header':title,

    }
    if selfProfile:
        context['selfProfile']=1
    context['user_role']=get_user_role(request.user)
    context['user_layout']=request.user
    # print(context)
    return render(request, 'profile.html',context)

@login_required
def edit_user_info(request):
    first_name=request.POST.get('first_name','')
    if first_name:
        request.user.first_name=first_name
        request.user.save()
    phone_number=request.POST.get('phone_number','')
    address=request.POST.get('address','')
    self_introdution=request.POST.get('self_introdution','')
    skill=request.POST.get('skill','')
    userInfo=db.User_info.objects.get(user=request.user)
    userInfo.phone_number=phone_number
    userInfo.address=address
    userInfo.self_introdution=self_introdution
    userInfo.skill=skill
    userInfo.save()
    return redirect('/profile?u='+request.user.username)
@login_required
def change_password(request):
    oldPassword=request.POST.get('oldPwd','')
    newPassword=request.POST.get('newPwd','')
    if not (newPassword and oldPassword):
        return JsonResponseError('Thiếu dữ liệu')
    if not check_password(oldPassword,request.user.password):  
        return JsonResponseError('Mật khẩu cũ không chính xác')
    if len(newPassword) <8:
        return JsonResponseError('Mật khẩu mới phải lớn hơn 8 ký tự')
    request.user.set_password(newPassword)
    request.user.save()
    return JsonResponseSuccess('Đổi mật khẩu thành công')