from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
import requests

User = get_user_model()

class SSOUserMiddleware:
    """
    Middleware to handle SSO user information.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for non-API requests
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Get the authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return self.get_response(request)
        
        # Extract the token
        token = auth_header.split(' ')[1]
        
        try:
            # Verify token with SSO service
            response = requests.post(
                settings.SSO_TOKEN_VERIFY_URL,
                json={"token": token},
                timeout=5
            )
            
            if response.status_code == 201:
                # Token is valid, get user information
                access_token = AccessToken(token)
                user_id = access_token.payload.get('user_id')
                email = access_token.payload.get('email')
                
                if user_id and email:
                    # Get or create user
                    user, created = User.objects.get_or_create(
                        id=user_id,
                        defaults={
                            'email': email,
                            'username': email,
                            'is_active': True
                        }
                    )
                    
                    # Set user on request
                    request.user = user
                    request._request.user = user  # For DRF
        except Exception:
            # If there's any error, just continue without setting the user
            pass
        
        return self.get_response(request) 