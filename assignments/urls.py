from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.assignment_list_view, name='list'),
    path('create/', views.assignment_create_view, name='create'),
    path('<int:pk>/', views.assignment_detail_view, name='detail'),
    path('pdf/<int:pk>/download/', views.download_pdf_view, name='download_pdf'),
]
