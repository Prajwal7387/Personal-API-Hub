from core.services.base import BaseApiService
from typing import List, Dict, Any, Optional
import requests

class GitHubService(BaseApiService):
    """
    Service layer specifically for GitHub API interactions.
    Responsibility: Fetch raw data and handle API-specific errors.
    """

    def __init__(self, api_token: str):
        # GitHub uses 'token' or 'Bearer' depending on context, 
        # but for REST API v3, 'token' in headers or 'Bearer' is standard.
        super().__init__(base_url='https://api.github.com', api_token=api_token)
        # Update session with GitHub specific headers
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Personal-API-Hub'
        })

    def fetch_data(self, endpoint: str = 'user/repos', params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Implementation of the abstract fetch_data method.
        Fetches all repositories for the authenticated user by default.
        """
        try:
            return self.get(endpoint, params=params)
        except requests.exceptions.HTTPError as e:
            # Re-raise with a more descriptive message or handle specifically
            raise Exception(f"GitHub API Error: {str(e)}")

    def get_raw_repositories(self) -> List[Dict[str, Any]]:
        """
        Wraps fetch_data for clarity in the normalization phase.
        """
        return self.fetch_data('user/repos')
