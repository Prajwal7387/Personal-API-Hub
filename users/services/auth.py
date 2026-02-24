from django.contrib.auth import get_user_model
from typing import Dict, Any

User = get_user_model()

class UserService:
    """
    Service layer for User-related business logic.
    """

    @staticmethod
    def register_user(user_data: Dict[str, Any]) -> User:
        """
        Logic for creating a new user.
        """
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email']
        )
        return user
