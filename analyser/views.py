from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Report, AnalysisResult
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
    alerts_found = sum(len(r.analysis.abnormalities) for r in reports if r.status == 'completed' and hasattr(r, 'analysis') and isinstance(r.analysis.abnormalities, list))
    
    context = {
        'reports': reports,
        'total_reports': total_reports,
        'analyzed_reports': analyzed_reports,
        'alerts_found': alerts_found
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
