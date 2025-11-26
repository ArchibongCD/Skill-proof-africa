# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json

@csrf_exempt
def register_user(request):
    """Handle user registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Check if username exists
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Username already exists'
                }, status=400)
            
            # Check if email exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Email already registered'
                }, status=400)
            
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Registration successful',
                'user_id': user.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def login_user(request):
    """Handle user login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'username': user.username,
                    'email': user.email
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid credentials'
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

@login_required
def logout_user(request):
    """Handle user logout"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})

@login_required
def user_profile(request):
    """Get user profile"""
    user = request.user
    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'wallet_address': user.wallet_address,
        'country': user.country,
        'bio': user.bio
    })

@csrf_exempt
@login_required
def update_wallet(request):
    """Update user's wallet address"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            wallet_address = data.get('wallet_address')
            
            user = request.user
            user.wallet_address = wallet_address
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Wallet address updated',
                'wallet_address': wallet_address
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)