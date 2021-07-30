from django.urls import path

from . import views

urlpatterns = [
    path('test-notifications/', views.index, name='test-notifications'),
    path('get-notifications/', views.get_notifications, name='get-notifications')
]