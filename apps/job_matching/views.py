import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.users.models import Profile
from ai_resume_platform.utils.ai_service import AIService

@login_required
def job_match(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.resume_url:
        messages.error(request, 'Please upload a resume first.')
        return redirect('resume_upload')
    
    # Increment jobs matched counter
    if 'jobs_matched' in request.session:
        request.session['jobs_matched'] += 1
    else:
        request.session['jobs_matched'] = 1
    
    context = {
        'profile': profile
    }
    
    return render(request, 'job_matching/job_match.html', context)

@login_required
def match_job(request):
    if request.method == 'POST':
        try:
            # Get job details from POST data
            job_title = request.POST.get('job_title', '')
            company = request.POST.get('company', '')
            job_level = request.POST.get('job_level', '')
            salary = request.POST.get('salary', '')
            job_description = request.POST.get('job_description', '')
            
            if not job_title or not job_description:
                return JsonResponse({'error': 'Job title and description are required'}, status=400)
            
            profile = Profile.objects.get(user=request.user)
            
            if not profile.resume_url:
                return JsonResponse({'error': 'No resume uploaded'}, status=400)
            
            # Initialize AI service
            ai_service = AIService()
            
            # Pass the Cloudinary URL and job details to the AI service
            resume_url = profile.resume_url
            
            # Create comprehensive job details
            job_details = {
                'title': job_title,
                'company': company,
                'level': job_level,
                'salary': salary,
                'description': job_description
            }
            
            # Call AI service to match job
            match_result = ai_service.match_job_from_url(resume_url, job_details)
            
            # Check if there was an error
            if 'error' in match_result:
                return JsonResponse({'error': match_result['error']}, status=500)
            
            return JsonResponse({'match': match_result})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def match_job_direct(request):
    """Match job directly with resume URL without storing data"""
    if request.method == 'POST':
        try:
            # Get job details from POST data
            job_title = request.POST.get('job_title', '')
            job_description = request.POST.get('job_description', '')
            job_employment_type = request.POST.get('job_employment_type', '')
            employer_name = request.POST.get('employer_name', '')
            job_city = request.POST.get('job_city', '')
            job_state = request.POST.get('job_state', '')
            
            if not job_title or not job_description:
                return JsonResponse({'error': 'Job title and description are required'}, status=400)
            
            profile = Profile.objects.get(user=request.user)
            
            if not profile.resume_url:
                return JsonResponse({'error': 'No resume uploaded'}, status=400)
            
            # Initialize AI service
            ai_service = AIService()
            
            # Pass the Cloudinary URL and job details to the AI service
            resume_url = profile.resume_url
            
            # Create comprehensive job details
            job_details = {
                'title': job_title,
                'company': employer_name,
                'level': job_employment_type,
                'description': job_description,
                'location': f"{job_city}, {job_state}" if job_city and job_state else (job_city or job_state or '')
            }
            
            # Call AI service to match job
            match_result = ai_service.match_job_from_url(resume_url, job_details)
            
            # Check if there was an error
            if 'error' in match_result:
                return JsonResponse({'error': match_result['error']}, status=500)
            
            return JsonResponse({'match': match_result})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)