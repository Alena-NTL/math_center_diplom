from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_queue_view, name='queue'),
    path('<int:pk>/', views.moderation_review_view, name='review'),
]
