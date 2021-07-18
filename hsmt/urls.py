from django.urls import path
from .views import (
    XFileListView,
    XFileCreateView,
    XFileDetailView,
    XFileDeleteView,
    XFileTypeListView,
    XFileTypeCreateView,
    XFileTypeDetailView,
    XFileChangeDetailView
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

    path('change/<int:pk>/',XFileChangeDetailView.as_view(), name='hsmt-change-detail'),

    path('type/',XFileTypeListView.as_view(), name='hsmt-type-list'),
    path('type/create/',XFileTypeCreateView.as_view(), name='hsmt-type-create'),
    path('type/<int:pk>/',XFileTypeDetailView.as_view(), name='hsmt-type-detail'),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)