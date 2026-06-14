from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task-list"),
    path('create/', views.create_task, name='create-task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle-task')
]
