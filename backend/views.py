# backend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from courses.models import Course
from certificates.models import Certificate

def home(request):
    """Landing page"""
    return render(request, 'index.html')

def courses_page(request):
    """Courses listing page"""
    return render(request, 'courses.html')

def course_detail(request, slug):
    """Single course detail page"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    return render(request, 'course_detail.html', {'course': course})

@login_required
def dashboard(request):
    """User dashboard - requires login"""
    return render(request, 'dashboard.html')

def login_page(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'login.html')

def register_page(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'register.html')

def logout_page(request):
    """Logout user and redirect to home"""
    logout(request)
    return redirect('/')

@login_required
def certificates_page(request):
    """User certificates page - redirect to dashboard for now"""
    return redirect('/dashboard')

def verify_certificate(request):
    """Public certificate verification page"""
    certificate = None
    error_message = None
    certificate_id = request.GET.get('id', '')
    
    if certificate_id:
        try:
            certificate = Certificate.objects.select_related('user', 'course').get(
                certificate_id=certificate_id
            )
        except Certificate.DoesNotExist:
            error_message = "Certificate not found. Please check the ID and try again."
    
    context = {
        'certificate': certificate,
        'error_message': error_message,
        'certificate_id': certificate_id,
    }
    
    return render(request, 'verify.html', context)