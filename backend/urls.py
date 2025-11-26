# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views  # Import views from backend folder

urlpatterns = [
    # Main pages (using views)
    path('', views.home, name='home'),
    path('courses/', views.courses_page, name='courses_page'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('about/', views.about_page, name='about'),
    path('certificates/', views.certificates_page, name='certificates_page'),
    path('verify/', views.verify_certificate, name='verify'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/certificates/', include('certificates.urls')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)