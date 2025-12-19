import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from apps.users.models import Profile
from ai_resume_platform.utils.ai_service import AIService

@login_required
def career_path(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.resume_url:
        messages.error(request, 'Please upload a resume first.')
        return redirect('resume_upload')
    
    # Increment career paths counter
    if 'career_paths' in request.session:
        request.session['career_paths'] += 1
    else:
        request.session['career_paths'] = 1
    
    return render(request, 'career_path/career.html', {'profile': profile})

@login_required
def plan_career(request):
    if request.method == 'POST':
        try:
            # Get form data
            career_goal = request.POST.get('career_goal', '')
            timeframe = request.POST.get('timeframe', '')
            preferred_industry = request.POST.get('preferred_industry', '')
            current_skill_level = request.POST.get('current_skill_level', '')
            learning_commitment = request.POST.get('learning_commitment', '')
            target_outcome = request.POST.get('target_outcome', '')
            
            profile = Profile.objects.get(user=request.user)
            
            if not profile.resume_url:
                return JsonResponse({'error': 'No resume uploaded'}, status=400)
            
            # Initialize AI service
            ai_service = AIService()
            
            # Create user inputs dictionary
            user_inputs = {
                'career_goal': career_goal,
                'timeframe': timeframe,
                'preferred_industry': preferred_industry,
                'current_skill_level': current_skill_level,
                'learning_commitment': learning_commitment,
                'target_outcome': target_outcome
            }
            
            # Call AI service to plan career with resume URL
            career_plan = ai_service.plan_career_from_url(profile.resume_url, user_inputs)
            
            # Check if there was an error
            if 'error' in career_plan:
                return JsonResponse({'error': career_plan['error']}, status=500)
            
            return JsonResponse({'career_plan': career_plan})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)