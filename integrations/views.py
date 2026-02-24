from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.sync import SyncService

from core.utils.responses import success_response, error_response

class SyncGitHubView(APIView):
    """
    Manually triggers the GitHub project data synchronization.
    """
    def post(self, request):
        try:
            # Trigger the sync orchestration service
            normalized_data = SyncService.sync_github_data(request.user)
            
            return success_response(
                data={"repo_count": normalized_data.get("repo_count")},
                message="GitHub synchronization completed successfully."
            )
            
        except ValueError as e:
            return error_response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response("Sync failed unexpectedly. Please try again later.", status.HTTP_500_INTERNAL_SERVER_ERROR)

class SyncSpotifyView(APIView):
    """
    Manually triggers the Spotify data synchronization.
    """
    def post(self, request):
        try:
            normalized_data = SyncService.sync_spotify_data(request.user)
            return success_response(
                data={"playlist_count": normalized_data.get("playlist_count")},
                message="Spotify synchronization completed successfully."
            )
        except ValueError as e:
            return error_response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response("Sync failed unexpectedly. Please try again later.", status.HTTP_500_INTERNAL_SERVER_ERROR)
