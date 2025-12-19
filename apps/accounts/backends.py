from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either 
    their username or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        
        # Try to find user by username first
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If not found by username, try to find by email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        
        # Check password
        if user.check_password(password):
            return user
        
        return None