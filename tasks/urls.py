from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('', views.TaskListView.as_view(), name="task_list"),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name="task_detail"),
    path('task/new/', views.TaskCreateView.as_view(), name="task_create"),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name="task_delete"),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name="task_update"),
]
