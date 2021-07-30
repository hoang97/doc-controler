from django.urls import path
from .views import (
    XFileListView,
    XFileCreateView,
    XFileDetailView,
    XFileDeleteView,
    XFileTypeListView,
    XFileTypeCreateView,
    XFileTypeDetailView,
    XFileChangeDetailView,
    get_permission_user_xfile,
    create_change_xfile,
    cancel_change_xfile,
    submit_change_xfile,
    check_change_xfile,
    reject_check_xfile,
    approve_change_xfile,
    reject_approve_xfile
)

# just for debug
from django.conf import settings
from django.conf.urls.static import static
#--------------------------#

urlpatterns = [
    path('',XFileListView.as_view(), name='hsmt-list'),
    path('create/',XFileCreateView.as_view(), name='hsmt-create'),
    path('xfile/<int:pk>/',XFileDetailView.as_view(), name='hsmt-detail'),
    path('xfile/<int:pk>/delete/',XFileDeleteView.as_view(), name='hsmt-delete'),
    path('xfile/<int:pk>/perm/',get_permission_user_xfile, name='hsmt-perm'),
    path('xfile/<int:pk>/create-change/',create_change_xfile, name='hsmt-create-change'),
    path('xfile/<int:pk>/cancel-change/',cancel_change_xfile, name='hsmt-cancel-change'),
    path('xfile/<int:pk>/submit/',submit_change_xfile, name='hsmt-submit'),
    path('xfile/<int:pk>/check/',check_change_xfile, name='hsmt-check'),
    path('xfile/<int:pk>/reject-check/',reject_check_xfile, name='hsmt-reject-check'),
    path('xfile/<int:pk>/approve/',approve_change_xfile, name='hsmt-approve'),
    path('xfile/<int:pk>/reject-approve/',reject_approve_xfile, name='hsmt-reject-approve'),

    path('change/<int:pk>/',XFileChangeDetailView.as_view(), name='hsmt-change-detail'),

    path('type/',XFileTypeListView.as_view(), name='hsmt-type-list'),
    path('type/create/',XFileTypeCreateView.as_view(), name='hsmt-type-create'),
    path('type/<int:pk>/',XFileTypeDetailView.as_view(), name='hsmt-type-detail'),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)