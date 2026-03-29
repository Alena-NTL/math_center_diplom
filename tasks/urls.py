from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list_view, name='list'),
    path('<int:pk>/', views.task_detail_view, name='detail'),
    path('create/', views.task_create_view, name='create'),
    path('<int:pk>/edit/', views.task_edit_view, name='edit'),
    path('<int:pk>/submit/', views.task_submit_view, name='submit'),
]
