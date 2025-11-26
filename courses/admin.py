# courses/admin.py

from django.contrib import admin
from .models import Course, Quiz, Question, UserProgress

class QuestionInline(admin.TabularInline):
    """
    Inline admin for questions in quiz
    """
    model = Question
    extra = 3

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['course', 'passing_score', 'time_limit']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer', 'points']
    list_filter = ['quiz']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'score', 'completed', 'completed_at']
    list_filter = ['completed', 'course']
    search_fields = ['user__username', 'course__title']