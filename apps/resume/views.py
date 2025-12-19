import cloudinary
import cloudinary.uploader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Resume
from apps.users.models import Profile

@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                request.FILES['resume'],
                folder=f"resumes/{request.user.id}",
                resource_type="raw",
                allowed_formats=['pdf']
            )
            
            # Save to database
            resume = Resume.objects.create(
                user=request.user,
                cloudinary_url=result['secure_url']
            )
            
            # Update user profile
            profile = Profile.objects.get(user=request.user)
            profile.resume_url = result['secure_url']
            profile.save()
            
            messages.success(request, 'Resume uploaded successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error uploading resume: {str(e)}')
            return redirect('resume_upload')
    
    return render(request, 'resume/upload.html')

@login_required
def delete_resume(request):
    if request.method == 'POST':
        try:
            # Delete from database
            Resume.objects.filter(user=request.user).delete()
            
            # Update user profile
            profile = Profile.objects.get(user=request.user)
            profile.resume_url = None
            profile.save()
            
            messages.success(request, 'Resume deleted successfully! You can now upload a new one.')
        except Exception as e:
            messages.error(request, f'Error deleting resume: {str(e)}')
    
    return redirect('profile')