from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.users.models import Profile

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})