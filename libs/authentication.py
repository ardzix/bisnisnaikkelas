import requests
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework import exceptions

User = get_user_model()

class SSOAuthentication(JWTAuthentication):
    """
    Custom authentication class that validates tokens using the SSO service.
    """
    
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        
        # Get user from token
        user = self.get_user(validated_token)
        
        return (user, validated_token)
    
    def get_validated_token(self, raw_token):
        """
        Validate the token using the SSO service.
        """
        try:
            # First try to validate locally
            token = AccessToken(raw_token.decode())
            
            # Then verify with SSO service
            response = requests.post(
                settings.SSO_TOKEN_VERIFY_URL,
                json={"token": raw_token.decode()},
                timeout=5
            )
            
            if response.status_code != 201:
                raise InvalidToken("Token validation failed with SSO service")
                
            return token
        except Exception as e:
            raise InvalidToken(str(e))
    
    def get_user(self, validated_token):
        """
        Get or create a user based on the token payload.
        """
        try:
            # Extract user information from token
            user_id = validated_token.payload.get('user_id')
            email = validated_token.payload.get('email')
            
            if not user_id or not email:
                raise exceptions.AuthenticationFailed('Invalid token payload')
            
            # Try to get existing user
            user, created = User.objects.get_or_create(
                id=user_id,
                defaults={
                    'email': email,
                    'username': email,  # Using email as username
                    'is_active': True
                }
            )
            
            return user
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e)) 