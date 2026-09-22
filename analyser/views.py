from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Report, AnalysisResult, MedicalDocument
from ai.parsers import extract_text_from_file
from ai.engine import analyze_medical_text

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    reports = request.user.reports.all().order_by('-uploaded_at')
    
    total_reports = reports.count()
    analyzed_reports = reports.filter(status='completed').count()
    
    # Calculate total alerts from analyzed reports
    alerts_found = 0
    
    # Aggregate historical trend data
    import re
    import json
    from collections import defaultdict
    
    trends_data = defaultdict(list)
    
    # Process reports chronologically for charts
    completed_reports = request.user.reports.filter(status='completed').order_by('uploaded_at')
    
    for report in completed_reports:
        if hasattr(report, 'analysis'):
            # Legacy field count
            if isinstance(report.analysis.abnormalities, list):
                alerts_found += len(report.analysis.abnormalities)
            
            # Combine all findings for trends
            findings = []
            if isinstance(report.analysis.all_findings, list) and report.analysis.all_findings:
                findings = report.analysis.all_findings
            elif isinstance(report.analysis.abnormalities, list):
                findings = report.analysis.abnormalities
                
            date_str = report.uploaded_at.strftime('%b %d, %Y')
            
            for item in findings:
                param = item.get('parameter')
                raw_value = item.get('value', '')
                
                if param and raw_value:
                    # Try to extract the first numeric sequence, handling decimals
                    match = re.search(r'[-+]?\d*\.\d+|\d+', str(raw_value))
                    if match:
                        numeric_val = float(match.group())
                        trends_data[param].append({
                            'date': date_str,
                            'value': numeric_val,
                            'status': item.get('status', 'Unknown')
                        })

    # Only keep parameters with more than one data point for trending
    trends_data = {k: v for k, v in trends_data.items() if len(v) > 1}
    
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = None
    
    context = {
        'reports': reports,
        'total_reports': total_reports,
        'analyzed_reports': analyzed_reports,
        'alerts_found': alerts_found,
        'trends_json': json.dumps(trends_data),
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def upload_report(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        report = Report.objects.create(user=request.user, file=file)
        
        # Analyze it
        text = extract_text_from_file(report.file.path)
        if text:
            ai_data = analyze_medical_text(text)
            AnalysisResult.objects.create(
                report=report,
                summary=ai_data.get('summary', ''),
                raw_text=text,
                insights=ai_data.get('insights', []),
                all_findings=ai_data.get('all_findings', []),
                abnormalities=ai_data.get('abnormalities', []),
                recommendations=ai_data.get('recommendations', [])
            )
            report.status = 'completed'
            report.save()
        else:
            report.status = 'failed'
            report.save()
            
        return redirect('report_detail', pk=report.pk)
    
    return render(request, 'upload.html')

@login_required
def report_detail(request, pk):
    try:
        report = Report.objects.get(pk=pk, user=request.user)
    except Report.DoesNotExist:
        return redirect('dashboard')
        
    try:
        analysis = report.analysis
    except AnalysisResult.DoesNotExist:
        analysis = None
        
    # Extract text on the fly if needed for display
    try:
        raw_text = extract_text_from_file(report.file.path) if report.file else ""
    except Exception:
        raw_text = "Could not read original file text."
        
    return render(request, 'report_detail.html', {'report': report, 'analysis': analysis, 'raw_text': raw_text})

@login_required
def document_list(request):
    category = request.GET.get('category', '')
    documents = request.user.medical_documents.all().order_by('-uploaded_at')
    if category:
        documents = documents.filter(category=category)
        
    context = {
        'documents': documents,
        'current_category': category,
        'categories': MedicalDocument.CATEGORY_CHOICES
    }
    return render(request, 'documents/document_list.html', context)

@login_required
def document_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        title = request.POST.get('title', file.name)
        category = request.POST.get('category', 'other')
        notes = request.POST.get('notes', '')
        
        MedicalDocument.objects.create(
            user=request.user,
            file=file,
            title=title,
            category=category,
            notes=notes
        )
        return redirect('document_list')
        
    context = {
        'categories': MedicalDocument.CATEGORY_CHOICES
    }
    return render(request, 'documents/document_upload.html', context)

@login_required
def document_delete(request, pk):
    try:
        document = MedicalDocument.objects.get(pk=pk, user=request.user)
        if request.method == 'POST':
            document.delete()
            return redirect('document_list')
    except MedicalDocument.DoesNotExist:
        pass
    return redirect('document_list')

import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

@login_required
def export_report_pdf(request, pk):
    try:
        report = Report.objects.get(pk=pk, user=request.user)
    except Report.DoesNotExist:
        return redirect('dashboard')
        
    try:
        analysis = report.analysis
    except AnalysisResult.DoesNotExist:
        return redirect('report_detail', pk=pk)
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=14))
    styles.add(ParagraphStyle(name='CustomHeading2', parent=styles['Heading2'], fontSize=14, spaceAfter=10, textColor=colors.HexColor('#0284c7')))
    styles.add(ParagraphStyle(name='AbnormalText', parent=styles['Normal'], textColor=colors.HexColor('#dc2626')))
    
    Story = []
    
    Story.append(Paragraph(f"MediReport Analysis for {request.user.username}", styles['CustomTitle']))
    Story.append(Paragraph(f"Date: {report.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    Story.append(Spacer(1, 24))
    
    # Summary
    Story.append(Paragraph("Summary", styles['CustomHeading2']))
    Story.append(Paragraph(analysis.summary, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Insights
    if isinstance(analysis.insights, list) and analysis.insights:
        Story.append(Paragraph("General Insights", styles['CustomHeading2']))
        for insight in analysis.insights:
            Story.append(Paragraph(f"• {insight}", styles['Normal']))
        Story.append(Spacer(1, 12))
        
    # Abnormalities
    findings = []
    if isinstance(analysis.all_findings, list) and analysis.all_findings:
        findings = analysis.all_findings
    elif isinstance(analysis.abnormalities, list):
        findings = analysis.abnormalities
        
    if findings:
        Story.append(Paragraph("Findings & Abnormalities", styles['CustomHeading2']))
        for item in findings:
            param = item.get('parameter', '')
            val = item.get('value', '')
            status = item.get('status', 'Unknown')
            explanation = item.get('explanation', '')
            
            p_style = styles['AbnormalText'] if status.lower() == 'abnormal' else styles['Normal']
            Story.append(Paragraph(f"<b>{param}</b>: {val} (Status: {status})", p_style))
            if explanation:
                Story.append(Paragraph(f"<i>{explanation}</i>", p_style))
            Story.append(Spacer(1, 6))
            
    # Recommendations
    if isinstance(analysis.recommendations, list) and analysis.recommendations:
        Story.append(Spacer(1, 12))
        Story.append(Paragraph("Recommendations", styles['CustomHeading2']))
        for rec in analysis.recommendations:
            Story.append(Paragraph(f"• {rec}", styles['Normal']))
            
    doc.build(Story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="MediReport_{report.id}.pdf"'
    
    return response

@login_required
def clinical_history(request):
    reports = request.user.reports.all().order_by('-uploaded_at')
    
    # We can also add basic filtering here if we want
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)
        
    return render(request, 'clinical_history.html', {'reports': reports, 'current_status': status_filter})

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'blood_type', 'height', 'weight', 'medical_conditions']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def bmi_calculator(request):
    return render(request, 'bmi_calculator.html')
