from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='resume_upload'),
    path('delete/', views.delete_resume, name='resume_delete'),
]