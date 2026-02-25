import requests
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseApiService(ABC):
    """
    Abstract Base Class for all external API integrations.
    """
    
    def __init__(self, base_url: str, api_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.session = requests.Session()
        if api_token:
            self.session.headers.update({
                'Authorization': f'Bearer {api_token}',
                'Accept': 'application/json'
            })

    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = self._get_url(endpoint)
        response = self.session.request(method, url, **kwargs)
        
        # In a real scenario, we'd handle specific status codes here
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request('DELETE', endpoint, **kwargs)

    @abstractmethod
    def fetch_data(self, *args, **kwargs) -> Any:
        """
        Main entry point for fetching data from the external source.
        """
        pass
