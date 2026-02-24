from integrations.repositories import ExternalAccountRepository, NormalizedDataRepository
from integrations.github.service import GitHubService
from integrations.spotify.service import SpotifyService
from .normalizer import normalize_github_data, normalize_spotify_data

class SyncService:
    """
    Orchestrates the Fetch -> Normalize -> Save pipeline.
    """
    _account_repo = ExternalAccountRepository()
    _normalized_repo = NormalizedDataRepository()

    @classmethod
    def sync_github_data(cls, user):
        """
        Manages the synchronization process for GitHub data.
        """
        # ... (github sync logic)
        account = cls._account_repo.get_by_provider(user, 'github')
        if not account:
            raise ValueError("No GitHub account linked for this user.")
            
        token = account.access_token
        github_service = GitHubService(api_token=token)
        raw_data = github_service.get_raw_repositories()
        normalized_content = normalize_github_data(raw_data)
        
        cls._normalized_repo.update_or_create_data(
            user=user,
            source='github',
            data=normalized_content
        )
        return normalized_content

    @classmethod
    def sync_spotify_data(cls, user):
        """
        Manages the synchronization process for Spotify data.
        """
        account = cls._account_repo.get_by_provider(user, 'spotify')
        if not account:
            raise ValueError("No Spotify account linked for this user.")
            
        token = account.access_token
        spotify_service = SpotifyService(api_token=token)
        
        playlists = spotify_service.get_user_playlists()
        top_artists = spotify_service.get_top_artists()
        
        normalized_content = normalize_spotify_data(playlists, top_artists)
        
        cls._normalized_repo.update_or_create_data(
            user=user,
            source='spotify',
            data=normalized_content
        )
        return normalized_content
