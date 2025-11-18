"""
Session management for the Tkinter client
"""
from api_client import APIClient


class Session:
    """Session class to manage user state and API client"""
    
    def __init__(self):
        self.api_client = APIClient()
        self.user = None
    
    def set_token(self, token: str):
        """Set JWT token for authenticated requests"""
        self.api_client.set_token(token)
    
    def set_user(self, user: dict):
        """Set user data"""
        self.user = user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.api_client.token is not None
    
    def logout(self):
        """Clear session data"""
        self.api_client.token = None
        self.user = None

