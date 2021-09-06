from django.urls import path

from . import views, api_views

urlpatterns = [
    path('test-notifications/', views.index, name='test-notifications'),
    path('get-notifications/', views.get_notifications, name='get-notifications'),
    path('api/notifications/', api_views.UserNotificationView.as_view(), name='get'),
]