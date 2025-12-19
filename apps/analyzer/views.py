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
def analyzer(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.resume_url:
        messages.error(request, 'Please upload a resume first.')
        return redirect('resume_upload')
    
    # Increment resumes analyzed counter
    if 'resumes_analyzed' in request.session:
        request.session['resumes_analyzed'] += 1
    else:
        request.session['resumes_analyzed'] = 1
    
    return render(request, 'analyzer/analyzer.html', {'profile': profile})

@login_required
def analyze_resume(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
            
            if not profile.resume_url:
                return JsonResponse({'error': 'No resume uploaded'}, status=400)
            
            # Initialize AI service
            ai_service = AIService()
            
            # Pass the Cloudinary URL to the AI service
            resume_url = profile.resume_url
            
            # Call AI service to analyze resume - THIS CALLS THE REAL API
            analysis = ai_service.analyze_resume_from_url(resume_url)
            
            # Log the response for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"AI Service returned: {analysis}")
            
            # Check if there was an error from the API
            if 'error' in analysis:
                logger.error(f"API Error: {analysis['error']}")
                return JsonResponse({'error': analysis['error']}, status=500)
            
            # Return the REAL analysis from OpenRouter API
            logger.error(f"Sending analysis to frontend: {analysis}")
            return JsonResponse({'analysis': analysis})
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Exception in analyze_resume: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)