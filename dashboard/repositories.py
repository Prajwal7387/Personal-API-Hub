from dashboard.models import CustomAPI
from core.repositories.base import BaseRepository
from typing import Optional

class CustomAPIRepository(BaseRepository[CustomAPI]):
    def __init__(self):
        super().__init__(CustomAPI)

    def get_by_endpoint(self, user, endpoint_name: str) -> Optional[CustomAPI]:
        try:
            return self.model.objects.get(user=user, endpoint_name=endpoint_name)
        except self.model.DoesNotExist:
            return None
            
    def get_recent_apis(self, user, limit: int = 5):
        return self.model.objects.filter(user=user).order_by('-created_at')[:limit]
