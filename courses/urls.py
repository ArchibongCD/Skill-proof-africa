# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<slug:slug>/', views.course_detail, name='detail'),
    path('<slug:slug>/quiz/', views.quiz_view, name='quiz'),
    path('<slug:slug>/submit/', views.submit_quiz, name='submit'),
    path('progress/', views.user_progress, name='progress'),
]