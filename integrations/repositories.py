from integrations.models import NormalizedData, ExternalAccount
from core.repositories.base import BaseRepository
from typing import Optional

class NormalizedDataRepository(BaseRepository[NormalizedData]):
    def __init__(self):
        super().__init__(NormalizedData)

    def get_user_source_data(self, user, source: str) -> Optional[NormalizedData]:
        try:
            return self.model.objects.get(user=user, source=source)
        except self.model.DoesNotExist:
            return None

    def update_or_create_data(self, user, source: str, data: dict):
        obj, created = self.model.objects.update_or_create(
            user=user,
            source=source,
            defaults={'data': data}
        )
        return obj, created

class ExternalAccountRepository(BaseRepository[ExternalAccount]):
    def __init__(self):
        super().__init__(ExternalAccount)

    def get_by_provider(self, user, provider: str) -> Optional[ExternalAccount]:
        try:
            return self.model.objects.get(user=user, provider=provider)
        except self.model.DoesNotExist:
            return None
