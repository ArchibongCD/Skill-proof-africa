# courses/models.py

from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Represents a skill-based course
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('blockchain', 'Blockchain'),
        ('business', 'Business'),
        ('ai', 'AI & Machine Learning'),
        ('data', 'Data Science'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.IntegerField(help_text="Estimated duration in minutes")
    content = models.TextField(help_text="Course content in markdown or HTML")
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Quiz(models.Model):
    """
    Quiz for each course - must pass to get certificate
    """
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='quiz')
    passing_score = models.IntegerField(default=70, help_text="Percentage needed to pass")
    time_limit = models.IntegerField(default=30, help_text="Time limit in minutes")
    
    def __str__(self):
        return f"Quiz for {self.course.title}"
    
    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    """
    Individual questions for quizzes
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1, 
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    points = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quiz.course.title} - {self.question_text[:50]}"
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class UserProgress(models.Model):
    """
    Tracks user progress through courses
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"