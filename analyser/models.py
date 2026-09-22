from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Report {self.id} for {self.user.username}"

class AnalysisResult(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='analysis')
    summary = models.TextField()
    raw_text = models.TextField(blank=True, null=True)
    insights = models.JSONField(default=list)
    all_findings = models.JSONField(default=list)
    abnormalities = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for Report {self.report.id}"

class MedicalDocument(models.Model):
    CATEGORY_CHOICES = (
        ('lab_result', 'Lab/Test Result'),
        ('prescription', 'Prescription'),
        ('certificate', 'Medical Certificate'),
        ('scan', 'Scan/Imaging'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_documents')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    file = models.FileField(upload_to='documents/')
    notes = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class UserProfile(models.Model):
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    medical_conditions = models.TextField(blank=True, null=True, help_text="Any known pre-existing conditions")
    
    def __str__(self):
        return f"Profile of {self.user.username}"
