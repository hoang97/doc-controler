from django.urls import path
from . import views, api_views

urlpatterns = [
    # Views
    path('task/list', views.task_list_view, name='task-list'),
    path('task/<int:task_id>', views.task_view, name='task'),

    # APIs
    path('get-tasks/', views.get_tasks, name='get-tasks'),
    path('get-mini-tasks/<int:task_id>', views.get_mini_tasks, name='get-task'),

    path('edit-task/', views.edit_task, name='edit-task'),
    path('edit-mini-task/', views.edit_mini_task, name='edit-mini-task'),

    path('add-task/', views.add_task, name='add-task'),
    path('add-mini-task/<int:task_id>', views.add_mini_task, name='add-mini-task'),

    path('delete-task/', views.delete_task, name='delete-task'),
    path('delete-mini-task/', views.delete_mini_task, name='delete-mini-task'),

    path('switch-status/', views.switch_status, name='switch-status'),
    path('switch-status-mini-task/', views.switch_status_mini_task, name='switch-status-mini-task'),

    # REST APIs
    path('api/task/', api_views.TaskListView.as_view()),
    path('api/task/create/', api_views.TaskCreateView.as_view()),
    path('api/task/<int:pk>/', api_views.TaskUpdateDestroyView.as_view()),
    path('api/task/<int:pk>/detail/', api_views.TaskRetrieveView.as_view()),

    path('api/task/<int:pk>/minitask/', api_views.MiniTaskListView.as_view()),
    path('api/task/<int:pk>/minitask/create/', api_views.MiniTaskCreateView.as_view()),
    path('api/task/<int:pk>/minitask/<int:minitask_id>/', api_views.MiniTaskUpdateDeleteView.as_view()),
    path('api/task/<int:pk>/minitask/<int:minitask_id>/detail/', api_views.MiniTaskRetrieveView.as_view()),
    path('api/task/<int:pk>/minitask/<int:minitask_id>/status/', api_views.MiniTaskSwitchStatus.as_view()),
]
