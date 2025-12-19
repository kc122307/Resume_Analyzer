from django.urls import path
from . import views

urlpatterns = [
    path('', views.career_path, name='career_path'),
    path('plan/', views.plan_career, name='plan_career'),
]