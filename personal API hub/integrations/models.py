from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ExternalAccount(models.Model):
    """
    Stores external API credentials for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='external_accounts')
    provider = models.CharField(max_length=50) # e.g., 'github'
    access_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} account for {self.user.username}"

class NormalizedData(models.Model):
    """
    Stores normalized data from various integration sources.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='normalized_data')
    source = models.CharField(max_length=50)
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Normalized Data"

    def __str__(self):
        return f"Normalized data from {self.source} for {self.user.username}"
