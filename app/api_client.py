"""
API Client wrapper for the Flask backend
Handles all API requests from the Tkinter client
"""
import requests
from typing import Optional, Dict, Any


class APIClient:
    """API Client for communicating with the Flask backend"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token if available"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def set_token(self, token: str):
        """Set the JWT token for authenticated requests"""
        self.token = token
    
    def register(self, email: str, username: str, password: str, handicap: int = 0) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User's email
            username: User's username
            password: User's password
            handicap: User's golf handicap (default 0)
            
        Returns:
            Response data including token and user info
        """
        response = requests.post(
            f"{self.base_url}/register",
            json={
                "email": email,
                "username": username,
                "password": password,
                "handicap": handicap
            }
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            self.token = data.get("token")
            return data
        else:
            raise Exception(response.json().get("error", "Registration failed"))
    
    def login(self, identifier: str, password: str) -> Dict[str, Any]:
        """
        Login with email/username and password
        
        Args:
            identifier: Email or username
            password: User's password
            
        Returns:
            Response data including token and user info
        """
        response = requests.post(
            f"{self.base_url}/login",
            json={
                "identifier": identifier,
                "password": password
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
            return data
        else:
            raise Exception(response.json().get("error", "Login failed"))
    
    def get_user(self) -> Dict[str, Any]:
        """Get current user's profile"""
        response = requests.get(
            f"{self.base_url}/user",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to get user"))
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get dashboard data"""
        response = requests.get(
            f"{self.base_url}/dashboard",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to get dashboard"))
    
    def get_lessons(self) -> Dict[str, Any]:
        """Get all available lessons"""
        response = requests.get(
            f"{self.base_url}/lessons",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to get lessons"))
    
    def get_lesson(self, lesson_id: str) -> Dict[str, Any]:
        """Get a specific lesson by ID"""
        response = requests.get(
            f"{self.base_url}/lesson/{lesson_id}",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to get lesson"))
    
    def submit_lesson(self, lesson_id: str, accuracy: float, mistakes_count: int, time_taken: int) -> Dict[str, Any]:
        """Submit lesson results"""
        response = requests.post(
            f"{self.base_url}/lesson/{lesson_id}",
            headers=self._get_headers(),
            json={
                "accuracy": accuracy,
                "mistakes_count": mistakes_count,
                "time_taken": time_taken
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to submit lesson"))
    
    def deduct_heart(self) -> Dict[str, Any]:
        """Deduct a heart (when answering wrong)"""
        response = requests.post(
            f"{self.base_url}/heart/deduct",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            data = response.json()
            if data.get("streak_reset"):
                raise Exception("No hearts remaining! Streak has been reset.")
            raise Exception(data.get("error", "Failed to deduct heart"))
    
    def get_leaderboard(self, skip: int = 0, limit: int = 50) -> Dict[str, Any]:
        """Get leaderboard with pagination"""
        response = requests.get(
            f"{self.base_url}/leaderboard?skip={skip}&limit={limit}",
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to get leaderboard"))
    
    def update_settings(self, email: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Update user settings"""
        update_data = {}
        if email:
            update_data["email"] = email
        if password:
            update_data["password"] = password
        
        response = requests.patch(
            f"{self.base_url}/settings",
            headers=self._get_headers(),
            json=update_data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to update settings"))
    
    def delete_account(self, password: str) -> Dict[str, Any]:
        """Delete user account"""
        response = requests.delete(
            f"{self.base_url}/settings",
            headers=self._get_headers(),
            json={"password": password}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json().get("error", "Failed to delete account"))
