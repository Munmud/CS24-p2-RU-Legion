from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

def get_user_from_token(token):
    """
    Function to get user from token using JWTAuthentication.
    
    Args:
        token (str): JWT token string.
    
    Returns:
        User object: User object if token is valid, None otherwise.
    """
    jwt_authentication = JWTAuthentication()

    try:
        # Attempt to authenticate the token
        validated_token = jwt_authentication.get_validated_token(token)
        
        # Get the user from the validated token
        user = jwt_authentication.get_user(validated_token)
        
        # Return the user
        return user
    
    except InvalidToken:
        # Token is invalid
        return None
    except AuthenticationFailed:
        # Authentication failed for some reason
        return None
