from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views, api_views

# just for debug
from django.conf import settings
from django.conf.urls.static import static
#--------------------------#

urlpatterns = [
    # Views
    path('login/',views.login_view, name='user-login'),
    path('logout/',views.logout_view, name='user-logout'),
    path('register/',views.register_view, name='user-register'),
    path('success/',views.success_view, name='user-success'),
    path('user/list/',views.user_list_view, name='user-list'),
    path('profile/', views.profile_view, name='user-profile'),
    path('group/list/', views.group_list_view, name='group-list'),
    
    # APIs
    path('register-api/', views.register_api, name='user-register-api'),
    path('get-users/', views.get_users, name='get-users'),
    path('activate-user/', views.activate_user, name='activate-user'),
    path('delete-user/', views.delete_user, name='delete-user'),
    path('edit-user-info/', views.edit_user_info, name='edit-user-info'),
    path('change-password/', views.change_password, name='change-password'),

    # REST APIs
    path('api/department/', api_views.DepartmentListView.as_view(), name='api_department_list'),
    path('api/department/change-pwd/', api_views.department_change_pwd, name='api_department_change_pwd'),
    path('api/department/login/', api_views.department_login, name='api_department_login'),

    path('api/position/', api_views.PositionListView.as_view(), name='api_list_position'),

    path('api/login/', TokenObtainPairView.as_view(), name='api_user_login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='api_user_refresh'),
    path('api/user/', api_views.UserListView.as_view(), name='api_user_list'),
    path('api/user/<int:pk>/', api_views.UserRetrieveUpdateView.as_view(), name='api_user_detail_update'),
    path('api/user/<int:pk>/manage/', api_views.UserManageView.as_view(), name='api_user_manage'),
    path('api/user/register/', api_views.UserRegisterForAnyView.as_view(), name='api_user_register'),
    path('api/user/register-for-other/', api_views.UserRegisterForOtherView.as_view(), name='api_user_register_for_other'),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)