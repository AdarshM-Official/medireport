from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_report, name='upload_report'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('history/', views.clinical_history, name='clinical_history'),
    path('report/<int:pk>/export/pdf/', views.export_report_pdf, name='export_report_pdf'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
]
