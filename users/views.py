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
    return user.info.position.id

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
    context={
        'breadcrumb': title,
        'h1header': title,
        'userGroup': request.user.info.position.name,
        'user_role': request.user.info.position.id,
        'user_layout': request.user
    }
    return render(request, 'users/user-list.html', context)

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
