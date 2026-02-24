from typing import List, Dict, Any
from core.services.base import BaseApiService

class GitHubService(BaseApiService):
    """
    Service for interacting with GitHub API.
    """
    
    def __init__(self, api_token: str = None):
        super().__init__(base_url='https://api.github.com', api_token=api_token)
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Personal-API-Hub'
        })

    def fetch_data(self, endpoint: str = 'user/repos', params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch repositories for the authenticated user or a specific endpoint.
        """
        return self.request('GET', endpoint, params=params)

    def get_user_repositories(self) -> List[Dict[str, Any]]:
        """
        Convenience method to get current user's repositories.
        """
        return self.fetch_data('user/repos')

    def get_repository_details(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get details for a specific repository.
        """
        return self.request('GET', f'repos/{owner}/{repo}')
