from django.urls import path
from . import api_views, views

# just for debug
from django.conf import settings
from django.conf.urls.static import static
#--------------------------#

urlpatterns = [
    # Views
    path('', views.target_list_view, name='index'),
    path('hsmt/list/', views.hsmt_list_view, name='hsmt-list'),
    path('hsmt/edit-detail/', views.hsmt_edit_detail, name='hsmt-detail'),
    path('target/list/', views.target_list_view, name='target-list'),

    # XFileType API
    path('api/hsmt-type/', api_views.XFileTypeListCreateView.as_view()),
    path('api/hsmt-type/<int:pk>/', api_views.XFileTypeRetrieveUpdateDestroyView.as_view()),
    # Target API
    path('api/target/', api_views.TargetListCreateView.as_view()),
    path('api/target/<int:pk>/', api_views.TargetRetrieveUpdateDestroy.as_view()),
    # XFile API
    path('api/hsmt/', api_views.XFileListView.as_view()),
    path('api/hsmt/create/', api_views.XFileCreateView.as_view()),
    path('api/hsmt/<int:pk>/perm/', api_views.XFilePermView.as_view()), # quyền của user với xfile
    path('api/hsmt/<int:pk>/perm-update/', api_views.XFilePermUpdateView.as_view()), # sửa đổi danh sách editors, checkers, approvers
    path('api/hsmt/<int:pk>/general/', api_views.XFileRetrieveDestroyView.as_view()),
    path('api/hsmt/<int:pk>/general-update/', api_views.XFileGeneralUpdateView.as_view()),
    path('api/hsmt/<int:pk>/content/', api_views.XFileContentRetrieveUpdateView.as_view()),
    #-------------------------xfile comments---------------------------------------------------------#
    path('api/hsmt/<int:pk>/comments/', api_views.XFileCommentListView.as_view()),
    path('api/hsmt/<int:pk>/comments/create/', api_views.XFileCommentCreateView.as_view()),
    path('api/hsmt/<int:pk>/comments/<int:comment_id>/', api_views.XFileCommentRetrieveUpdateDestroyView.as_view()),
    #-------------------------attack logs---------------------------------------------------------#
    path('api/hsmt/<int:pk>/attacklogs/', api_views.AttackLogListView.as_view()),
    path('api/hsmt/<int:pk>/attacklogs/create/', api_views.AttackLogCreateView.as_view()),
    path('api/hsmt/<int:pk>/attacklogs/<int:attacklog_id>/', api_views.AttackLogRetrieveUpdateDeleteView.as_view()),
    #-------------------------xfile changes---------------------------------------------------------#
    path('api/hsmt/<int:pk>/changes/', api_views.XFileChangeListView.as_view()),
    path('api/hsmt/<int:pk>/changes/<int:version>/', api_views.XFileChangeRetrieveUpdateView.as_view()),
    #-------------------------xfile functions---------------------------------------------------------#
    path('api/hsmt/<int:pk>/create-change/',api_views.create_change_xfile, name='hsmt-create-change'),
    path('api/hsmt/<int:pk>/cancel-change/',api_views.cancel_change_xfile, name='hsmt-cancel-change'),
    path('api/hsmt/<int:pk>/submit/',api_views.submit_change_xfile, name='hsmt-submit'),
    path('api/hsmt/<int:pk>/check/',api_views.check_change_xfile, name='hsmt-check'),
    path('api/hsmt/<int:pk>/reject-check/',api_views.reject_check_xfile, name='hsmt-reject-check'),
    path('api/hsmt/<int:pk>/approve/',api_views.approve_change_xfile, name='hsmt-approve'),
    path('api/hsmt/<int:pk>/reject-approve/',api_views.reject_approve_xfile, name='hsmt-reject-approve'),
    
    # ------------------------------------------------------------------------------#
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)