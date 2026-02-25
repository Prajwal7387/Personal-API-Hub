from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAPI(models.Model):
    """
    User-defined API endpoint configuration.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_apis')
    endpoint_name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.endpoint_name} ({self.user.username})"
