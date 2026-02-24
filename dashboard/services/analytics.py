from typing import Dict, Any
from dashboard.repositories import CustomAPIRepository
from integrations.repositories import NormalizedDataRepository, ExternalAccountRepository

class AnalyticsService:
    """
    Service layer for dashboard analytics logic.
    """
    _api_repo = CustomAPIRepository()
    _normalized_repo = NormalizedDataRepository()
    _account_repo = ExternalAccountRepository()

    @classmethod
    def get_overview_data(cls, user) -> Dict[str, Any]:
        accounts_count = len(cls._account_repo.filter(user=user))
        custom_apis_count = len(cls._api_repo.filter(user=user))
        
        total_repos = 0
        github_data = cls._normalized_repo.get_user_source_data(user, 'github')
        if github_data:
            total_repos = github_data.data.get('repo_count', 0)

        return {
            "accounts_linked": accounts_count,
            "total_repositories": total_repos,
            "custom_apis_defined": custom_apis_count
        }

    @classmethod
    def get_activity_data(cls, user) -> Dict[str, Any]:
        github_data = cls._normalized_repo.get_user_source_data(user, 'github')
        last_sync = github_data.updated_at if github_data else None
        
        recent_configs = cls._api_repo.get_recent_apis(user)
        config_list = [{"name": cfg.endpoint_name, "created_at": cfg.created_at} for cfg in recent_configs]

        return {
            "last_sync": last_sync,
            "recent_custom_apis": config_list,
            "active_integrations": ["github"] if github_data else []
        }
