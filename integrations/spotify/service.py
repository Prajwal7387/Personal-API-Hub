from core.services.base import BaseApiService
from typing import List, Dict, Any, Optional

class SpotifyService(BaseApiService):
    """
    Service layer specifically for Spotify API interactions.
    Responsibility: Fetch raw music/player data using authenticated requests.
    """

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(base_url="https://api.spotify.com/v1", api_token=api_token)

    def fetch_data(self, endpoint: str, **kwargs) -> Any:
        return self.get(endpoint, **kwargs)

    def get_user_playlists(self) -> List[Dict[str, Any]]:
        """
        Fetches the current user's playlists.
        """
        response = self.get("me/playlists")
        return response.get('items', [])

    def get_top_artists(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetches the current user's top artists.
        """
        response = self.get("me/top/artists", params={'limit': limit})
        return response.get('items', [])

    def get_recently_played(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetches the current user's recently played tracks.
        """
        response = self.get("me/player/recently-played", params={'limit': limit})
        return response.get('items', [])
