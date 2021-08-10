from django.urls import path
from .views import (
    UserLoginView, 
    UserLogoutView, 
    UserRegisterView, 
    UserProfileView,
    UserProfileUpdate,
    login_view,
    logout_view,
    register_view,
    success_view,
    register_api,
    user_list_view,
    get_users
)

# just for debug
from django.conf import settings
from django.conf.urls.static import static
#--------------------------#

urlpatterns = [
    # Views
    path('login/',login_view, name='user-login'),
    path('logout/',logout_view, name='user-logout'),
    path('register/',register_view, name='user-register'),
    path('success/',success_view, name='user-success'),
    path('user/list/',user_list_view, name='user-list'),
    path('user/<int:pk>/profile/',UserProfileView.as_view(), name='user-profile'),
    path('user/<int:pk>/update/',UserProfileUpdate.as_view(), name='user-update'),

    # APIs
    path('register-api/',register_api, name='user-register-api'),
    path('get-users/',get_users, name='get-users'),

]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)