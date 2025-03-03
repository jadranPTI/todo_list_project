from django.urls import path
from .views import TaskListCreateView, AdminTaskListView, TaskGetUpdateDeleteView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # User-specific tasks
    path('tasks/admin/', AdminTaskListView.as_view(), name='admin-task-list'),  # Admin-only view
    path('tasks/<int:pk>/', TaskGetUpdateDeleteView.as_view(), name='task-detail-update-delete'),  # Task operations
]
