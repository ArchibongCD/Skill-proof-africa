# courses/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Quiz, Question, UserProgress
from certificates.models import Certificate
import json

def course_list(request):
    """List all active courses"""
    courses = Course.objects.filter(is_active=True)
    
    courses_data = [{
        'id': course.id,
        'title': course.title,
        'slug': course.slug,
        'description': course.description,
        'category': course.category,
        'difficulty': course.difficulty,
        'duration': course.duration,
    } for course in courses]
    
    return JsonResponse({'courses': courses_data})

def course_detail(request, slug):
    """Get course details"""
    course = get_object_or_404(Course, slug=slug)
    
    course_data = {
        'id': course.id,
        'title': course.title,
        'slug': course.slug,
        'description': course.description,
        'category': course.category,
        'difficulty': course.difficulty,
        'duration': course.duration,
        'content': course.content,
    }
    
    return JsonResponse({'course': course_data})

@login_required
def quiz_view(request, slug):
    """Get quiz questions for a course"""
    course = get_object_or_404(Course, slug=slug)
    
    try:
        quiz = course.quiz
        questions = quiz.questions.all()
        
        questions_data = [{
            'id': q.id,
            'question_text': q.question_text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'points': q.points,
        } for q in questions]
        
        return JsonResponse({
            'quiz': {
                'passing_score': quiz.passing_score,
                'time_limit': quiz.time_limit,
                'questions': questions_data
            }
        })
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'No quiz found for this course'}, status=404)

@csrf_exempt
@login_required
def submit_quiz(request, slug):
    """Submit quiz answers and calculate score"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    course = get_object_or_404(Course, slug=slug)
    quiz = get_object_or_404(Quiz, course=course)
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})  # {question_id: answer}
        
        # Calculate score
        total_points = 0
        earned_points = 0
        
        for question in quiz.questions.all():
            total_points += question.points
            user_answer = answers.get(str(question.id))
            
            if user_answer == question.correct_answer:
                earned_points += question.points
        
        score = int((earned_points / total_points) * 100) if total_points > 0 else 0
        passed = score >= quiz.passing_score
        
        # Update or create user progress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'score': score}
        )
        
        if not created:
            progress.score = max(progress.score, score)
        
        if passed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
            
            # Create certificate
            certificate, cert_created = Certificate.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={'score': score}
            )
            
            return JsonResponse({
                'success': True,
                'passed': True,
                'score': score,
                'certificate_id': certificate.certificate_id,
                'message': 'Congratulations! You passed!'
            })
        else:
            progress.save()
            return JsonResponse({
                'success': True,
                'passed': False,
                'score': score,
                'message': f'You scored {score}%. Pass mark is {quiz.passing_score}%'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def user_progress(request):
    """Get user's progress across all courses"""
    progress = UserProgress.objects.filter(user=request.user).select_related('course')
    
    progress_data = [{
        'course': {
            'title': p.course.title,
            'slug': p.course.slug,
        },
        'completed': p.completed,
        'score': p.score,
        'started_at': p.started_at.isoformat(),
        'completed_at': p.completed_at.isoformat() if p.completed_at else None
    } for p in progress]
    
    return JsonResponse({'progress': progress_data})