from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_match, name='job_match'),
    path('match/', views.match_job, name='match_job'),
    path('match-direct/', views.match_job_direct, name='match_job_direct'),
]