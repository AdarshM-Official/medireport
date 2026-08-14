from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_report, name='upload_report'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
]
