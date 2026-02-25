from django.urls import path
from .views import SyncGitHubView, SyncSpotifyView

urlpatterns = [
    path('github/sync/', SyncGitHubView.as_view(), name='github_sync'),
    path('spotify/sync/', SyncSpotifyView.as_view(), name='spotify_sync'),
]
