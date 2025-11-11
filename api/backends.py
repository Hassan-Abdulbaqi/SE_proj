"""
Custom authentication backend for mobile number authentication
"""
from django.contrib.auth.backends import ModelBackend
from .models import User


class MobileNumberBackend(ModelBackend):
    """
    Authenticate using mobile number instead of username.
    """
    
    def authenticate(self, request, mobile_number=None, password=None, **kwargs):
        """
        Authenticate a user based on mobile number and password.
        """
        if mobile_number is None or password is None:
            return None
        
        try:
            user = User.objects.get(mobile_number=mobile_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            User().set_password(password)
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

