from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import (
    XFile, 
    XFileChange, 
    Comment,
    XFileType,
    STATUS,
)
# Create your views here.
class XFileCreateView(CreateView):
    template_name = 'hsmt/create.html'
    model = XFile
    fields = ['code', 'description','type', 'targets', 'editors', 'checkers', 'approvers']
    success_url = reverse_lazy('hsmt-list')

    def form_valid(self, form):
        form.instance.department = self.request.user.info.department
        form.instance.content = form.instance.type.example_content
        httpresponse = super().form_valid(form)
        form.instance.create_change(change_name='Khởi tạo', by=self.request.user)
        form.save()
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