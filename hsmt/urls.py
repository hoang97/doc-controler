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
    # LCRUD - list, create, retrieve, update, destroy
    path('api/hsmt-type/', api_views.XFileTypeListCreateView.as_view(), name='api_xfile_type_L'),
    path('api/hsmt-type/<int:pk>/', api_views.XFileTypeRetrieveUpdateDestroyView.as_view(), name='api_xfile_type_RUD'),
    # Target API
    path('api/target/', api_views.TargetListCreateView.as_view(), name='api_target_LC'),
    path('api/target/<int:pk>/', api_views.TargetRetrieveUpdateDestroy.as_view(), name='api_target_RUD'),
    # XFile API
    path('api/hsmt/', api_views.XFileListView.as_view(), name='api_xfile_L'),
    path('api/hsmt/create/', api_views.XFileCreateView.as_view(), name='api_xfile_C'),
    path('api/hsmt/<int:pk>/perm/', api_views.XFilePermView.as_view(), name='api_xfile_perm'), # quyền của user với xfile
    path('api/hsmt/<int:pk>/perm-update/', api_views.XFilePermUpdateView.as_view(), name='api_xfile_U_perm'), # sửa đổi danh sách editors, checkers, approvers
    path('api/hsmt/<int:pk>/general/', api_views.XFileRetrieveDestroyView.as_view(), name='api_xfile_RD_general'),
    path('api/hsmt/<int:pk>/general-update/', api_views.XFileGeneralUpdateView.as_view(), name='api_xfile_U_general'),
    path('api/hsmt/<int:pk>/content/', api_views.XFileContentRetrieveUpdateView.as_view(), name='api_xfile_RU_content'),
    #-------------------------xfile comments---------------------------------------------------------#
    path('api/hsmt/<int:pk>/comments/', api_views.XFileCommentListView.as_view(), name='api_xfile_L_comment'),
    path('api/hsmt/<int:pk>/comments/create/', api_views.XFileCommentCreateView.as_view(), name='api_xfile_C_comment'),
    path('api/hsmt/<int:pk>/comments/<int:comment_id>/', api_views.XFileCommentRetrieveUpdateDestroyView.as_view(), name='api_xfile_RUD_comment'),
    #-------------------------attack logs---------------------------------------------------------#
    path('api/hsmt/<int:pk>/attacklogs/', api_views.AttackLogListView.as_view(), name='api_xfile_L_attacklog'),
    path('api/hsmt/<int:pk>/attacklogs/create/', api_views.AttackLogCreateView.as_view(), name='api_xfile_C_attacklog'),
    path('api/hsmt/<int:pk>/attacklogs/<int:attacklog_id>/', api_views.AttackLogRetrieveUpdateDeleteView.as_view(), name='api_xfile_RUD_attacklog'),
    #-------------------------xfile changes---------------------------------------------------------#
    path('api/hsmt/<int:pk>/changes/', api_views.XFileChangeListView.as_view(), name='api_xfile_L_change'),
    path('api/hsmt/<int:pk>/changes/<int:version>/', api_views.XFileChangeRetrieveUpdateView.as_view(), name='api_xfile_RU_change'),
    #-------------------------xfile functions---------------------------------------------------------#
    path('api/hsmt/<int:pk>/create-change/',api_views.XFileChangeCreateView.as_view(), name='hsmt-create-change'),
    path('api/hsmt/<int:pk>/cancel-change/',api_views.XFileChangeCancelView.as_view(), name='hsmt-cancel-change'),
    path('api/hsmt/<int:pk>/submit/',api_views.XFileChangeSubmitView.as_view(), name='hsmt-submit'),
    path('api/hsmt/<int:pk>/check/',api_views.XFileChangeCheckView.as_view(), name='hsmt-check'),
    path('api/hsmt/<int:pk>/reject-check/',api_views.XFileChangeRejectCheckView.as_view(), name='hsmt-reject-check'),
    path('api/hsmt/<int:pk>/approve/',api_views.XFileChangeApproveView.as_view(), name='hsmt-approve'),
    path('api/hsmt/<int:pk>/reject-approve/',api_views.XFileChangeRejectApproveView.as_view(), name='hsmt-reject-approve'),
    
    # ------------------------------------------------------------------------------#
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)