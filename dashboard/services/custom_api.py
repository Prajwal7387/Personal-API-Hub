from typing import Dict, Any
from ..models import CustomAPI
from dashboard.repositories import CustomAPIRepository
from integrations.repositories import NormalizedDataRepository

class CustomAPIService:
    """
    Service layer for Custom API operations.
    """
    _api_repo = CustomAPIRepository()
    _normalized_repo = NormalizedDataRepository()

    @classmethod
    def execute_custom_api(cls, user, endpoint_name: str) -> Dict[str, Any]:
        custom_api = cls._api_repo.get_by_endpoint(user, endpoint_name)
        if not custom_api:
            raise ValueError("Custom API endpoint not found.")
        
        config = custom_api.config
        data_type = config.get('type', 'coding_stats')
        fields = config.get('fields', [])

        source = 'github' if data_type == 'coding_stats' else None
        
        normalized_entry = cls._normalized_repo.get_user_source_data(user, source)
        if not normalized_entry:
            raise ValueError(f"No normalized data found for source '{source}'. Please sync first.")

        raw_data = normalized_entry.data
        response_data = {field: raw_data.get(field) for field in fields} if fields else raw_data

        return {
            "endpoint": endpoint_name,
            "type": data_type,
            "data": response_data
        }

    @staticmethod
    def create_custom_api(user, data: Dict[str, Any]) -> CustomAPI:
        """
        Logic for creating a new custom API.
        """
        # Validations can be added here
        return CustomAPI.objects.create(user=user, **data)
