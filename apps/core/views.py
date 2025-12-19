from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.users.models import Profile

def home(request):
    """Landing page for unauthenticated users"""
    return render(request, 'landing/index.html')

@login_required
def dashboard(request):
    """Main dashboard for authenticated users"""
    profile = Profile.objects.get(user=request.user)
    
    # Get activity counts from session or initialize to 0
    resumes_analyzed = request.session.get('resumes_analyzed', 0)
    jobs_matched = request.session.get('jobs_matched', 0)
    career_paths = request.session.get('career_paths', 0)
    resumes_built = request.session.get('resumes_built', 0)
    
    context = {
        'profile': profile,
        'resumes_analyzed': resumes_analyzed,
        'jobs_matched': jobs_matched,
        'career_paths': career_paths,
        'resumes_built': resumes_built
    }
    return render(request, 'dashboard/home.html', context)