from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyzer, name='analyzer'),
    path('analyze/', views.analyze_resume, name='analyze_resume'),
]