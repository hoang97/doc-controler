from users.models import UserInfor
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

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
        'title': 'Blog Controller Login'
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