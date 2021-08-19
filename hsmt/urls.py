from django.urls import path
from . import views
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
    # old xfile views
    # path('',XFileListView.as_view(), name='hsmt-list'),
    path('create/',XFileCreateView.as_view(), name='hsmt-create'),
    path('xfile/<int:pk>/',XFileDetailView.as_view(), name='hsmt-detail'),
    path('xfile/<int:pk>/delete/',XFileDeleteView.as_view(), name='hsmt-delete'),
    # old xfile APIs
    path('xfile/<int:pk>/perm/',get_permission_user_xfile, name='hsmt-perm'),
    path('xfile/<int:pk>/create-change/',create_change_xfile, name='hsmt-create-change'),
    path('xfile/<int:pk>/cancel-change/',cancel_change_xfile, name='hsmt-cancel-change'),
    path('xfile/<int:pk>/submit/',submit_change_xfile, name='hsmt-submit'),
    path('xfile/<int:pk>/check/',check_change_xfile, name='hsmt-check'),
    path('xfile/<int:pk>/reject-check/',reject_check_xfile, name='hsmt-reject-check'),
    path('xfile/<int:pk>/approve/',approve_change_xfile, name='hsmt-approve'),
    path('xfile/<int:pk>/reject-approve/',reject_approve_xfile, name='hsmt-reject-approve'),
    # old change views
    path('change/<int:pk>/',XFileChangeDetailView.as_view(), name='hsmt-change-detail'),
    # old type views
    path('type/',XFileTypeListView.as_view(), name='hsmt-type-list'),
    path('type/create/',XFileTypeCreateView.as_view(), name='hsmt-type-create'),
    path('type/<int:pk>/',XFileTypeDetailView.as_view(), name='hsmt-type-detail'),

# ------------------------------------------------------------------------------

    # new xfile views
    path('hsmt/list/', views.hsmt_list, name='hsmt-list'),
    path('get-xfiles/', views.get_xfiles, name='get-xfiles'),
    # path('hsmt/filter/', views.hsmt_filter,name='hsmt-filter'),
    path('hsmt/edit-detail/', views.hsmt_edit_detail, name='edit-detail'),
    path('hsmt/perm/', views.get_perm_user_xfile, name='get-xfile-perm'),
    path('get-xfile-by-id/', views.get_xfile_by_id, name='get-xfile-by-id'),
    path('get-xfile-user-role/', views.get_xfile_user_role, name='get-xfile-user-role'),

    #XFileChange API
    path('get-xfile-update/', views.get_xfile_update, name='get_xfile_update'),

    #target-type-views
    path('', views.target_type_list, name='list_target'),
    
    path('target-type/list', views.target_type_list, name='list_target'),
    path('add-edit-target-type', views.add_edit_target_type, name='add-target-type'),
    path('get-all-target-types', views.get_all_target_types, name='get-all-target-types'),
    path('get-target-type-by-type', views.get_target_type_by_type, name='get-all-target-types'),
    path('get-target-type-by-id', views.get_target_type_by_id, name='get-target-type-by-id'),
    path('delete-target-type', views.delete_target_type, name='delete-target-type'),

]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)