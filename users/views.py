from django.urls.base import reverse
from users.models import Department, Position, UserInfor
from django.shortcuts import get_object_or_404, redirect, render
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
from django.contrib.auth.hashers import check_password

# LIST_GROUPS=[
#     "Trợ Lý",
#     "Trưởng Phòng",
#     "Cục Trưởng"
# ]

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
            user.info.position = Position.objects.get(alias='tl')
            user.info.save()
            return JsonResponseSuccess('Tạo tài khoản thành công!')
    return JsonResponseError(msg)

def get_user_role(user):
    '''
    1 - trợ lí, alias=tl
    2 - trưởng phòng, alias=tp
    3 - giám đốc, alias=gd
    '''
    return str(user.info.position.id)

@login_required
def get_users(request):
    '''
    Get users by department
    '''
    user_info = request.user.info
    # Retrive user department
    data={
        'users':[],
        'owner_group':[user_info.position.name]
    }
    # List of user in department
    queryset = UserInfor.objects.filter(department=user_info.department).select_related('user').select_related('position')

    for user_info in queryset:
        data['users'].append({
            'id': user_info.user.id,
            'first_name': user_info.user.first_name,
            'last_login': user_info.user.last_login,
            'date_joined': user_info.user.date_joined,
            'username': user_info.user.username,
            'is_active': user_info.user.is_active,
            'groups': [user_info.position.name],
        })

    return JsonResponseSuccess(data)

@login_required
def activate_user(request):
    if request.method == "POST":
        # Chỉ trưởng phòng mới được kích hoạt tài khoản
        if request.user.info.position.alias != 'tp':
            return JsonResponseError('Không đủ thẩm quyền')
        
        userId=request.POST.get('userId','')
        if not userId:
            return JsonResponseError('Không đủ dữ liệu')
        userForChanged=User.objects.get(id=userId)
        if (userForChanged==request.user):
            return JsonResponseError('Không thể huỷ kích hoạt chính mình')
        if (userForChanged.info.department!=request.user.info.department):
            return JsonResponseError('Không thuộc phòng của bạn')
        userForChanged.is_active=not userForChanged.is_active
        userForChanged.save()
        return JsonResponseSuccess('Thành công')
    
    return JsonResponseError('')
    
@login_required 
def delete_user(request):
    if request.method == "POST":
        # Chỉ trưởng phòng mới được xóa tài khoản
        if request.user.info.position.alias != 'tp':
            return JsonResponseError('Không đủ thẩm quyền')
        
        userId=request.POST.get('userId','')
        if not userId:
            return JsonResponseError('Không đủ dữ liệu')
        userForDelete=User.objects.get(id=userId)
        if (userForDelete==request.user):
            return JsonResponseError('Không thể xóa chính mình')
        if (userForDelete.info.department!=request.user.info.department):
            return JsonResponseError('Không thuộc phòng của bạn')
        
        userForDelete.delete()
        return JsonResponseSuccess('Thành công')
    
    return JsonResponseError('')

@login_required
def edit_user_info(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name','')
        phone_number=request.POST.get('phone_number','')
        address=request.POST.get('address','')
        self_introduction=request.POST.get('self_introduction','')
        skill=request.POST.get('skill','')

        user = request.user
        userInfo = user.info
        if first_name:
            user.first_name = first_name
        userInfo.phone_number = phone_number
        userInfo.address = address
        userInfo.self_introduction = self_introduction
        userInfo.skill = skill
        user.save()

    return redirect('/profile?u='+request.user.username)

@login_required
def change_password(request):
    if request.method == "POST":
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

    return JsonResponseError('')

# Create your views here.
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
            user.info.position = Position.objects.get(alias='tl')
            user.info.save()
            return redirect(reverse('user-success') + f'?departmentNumber={departmentNumber}')

    context = {
        'msg': msg,
        'h1header': 'Đăng ký tài khoản',
        'department_list': Department.objects.exclude(alias='giamdoc')
    }
    return render(request, 'users/register.html', context)

@login_required
def user_list_view(request):
    title='Danh sách người dùng'
    userGroup=[request.user.info.department]
    context={'breadcrumb':title,'h1header':title,'userGroup':userGroup}
    # Quản lý Quyền
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user
    return render(request, 'users/user-list.html',context)

@login_required
def profile_view(request):
    userName=request.GET.get('u','')
    selfProfile=False
    if (request.user.username==userName):
        selfProfile=True
    user = get_object_or_404(User.objects.all().select_related('info').prefetch_related('xfiles_can_edit'), username=userName)
    userInfo = user.info

    totalXfile = user.xfiles_can_edit.count()

    group_name = userInfo.department.name
    title='Trang cá nhân'
    context={
        'user':{
            'username': user.username,
            'first_name': user.first_name,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'group_name': userInfo.position.name,
            'totalXfile': totalXfile
        },
        'userInfo':{
            'skill':userInfo.skill,
            'address':userInfo.address,
            'phone_number':userInfo.phone_number,
            'self_introduction':userInfo.self_introduction
        },
        'breadcrumb':title,
        'h1header':title,
    }
    if selfProfile:
        context['selfProfile']=1
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user
    # print(context)
    return render(request, 'users/profile.html',context)

@login_required
def group_list_view(request):
    title='Nhóm người dùng'
    context={
    'breadcrumb':title,
    'h1header':title
    }
    context['user_role']=str(request.user.info.position.id)
    context['user_layout']=request.user

    return render(request, 'users/group-list.html',context)

# Old views here
def display_form_error(request, errors):
    for obj, err in errors.items():
        msg = f"{obj}: {err[0]}"
        messages.error(request, msg)

class UserLoginView(LoginView):
    template_name = 'users/old/login.html'
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
    template_name = 'users/old/logout.html'
    next_page = 'user-login'
    extra_context = {
        'title': 'Blog Controller Logout'
    }

class UserRegisterView(CreateView):
    template_name = 'users/old/register.html'
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
    template_name = 'users/old/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Profile'
        return context

class UserProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/old/update.html'
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
