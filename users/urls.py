from django.urls import path
from .views import (
    UserLoginView, 
    UserLogoutView, 
    UserRegisterView, 
    UserProfileView,
    UserProfileUpdate,
)

# just for debug
from django.conf import settings
from django.conf.urls.static import static
#--------------------------#

urlpatterns = [
    path('login/',UserLoginView.as_view(), name='user-login'),
    path('logout/',UserLogoutView.as_view(), name='user-logout'),
    path('register/',UserRegisterView.as_view(), name='user-register'),
    path('user/<int:pk>/profile/',UserProfileView.as_view(), name='user-profile'),
    path('user/<int:pk>/update/',UserProfileUpdate.as_view(), name='user-update'),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)