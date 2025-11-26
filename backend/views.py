# backend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from courses.models import Course

def home(request):
    """Landing page"""
    return render(request, 'home.html')

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

def about_page(request):
    """About page - for now just redirect to home"""
    # We'll build this page later if needed
    return redirect('/')

@login_required
def certificates_page(request):
    """User certificates page - redirect to dashboard for now"""
    return redirect('/dashboard')

def verify_certificate(request):
    """Public certificate verification page"""
    # We'll build this later
    return redirect('/')