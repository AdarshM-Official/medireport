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
