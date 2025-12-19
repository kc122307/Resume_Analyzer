from django.urls import path
from . import views

urlpatterns = [
    path('', views.builder, name='builder'),
    path('generate/', views.generate_resume, name='generate_resume'),
    path('download/<str:filename>/', views.download_resume, name='download_resume'),
]