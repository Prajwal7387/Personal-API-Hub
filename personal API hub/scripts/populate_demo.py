import os
import django
import json
from datetime import datetime

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_api_hub.settings')
django.setup()

from django.contrib.auth.models import User
from integrations.models import ExternalAccount, NormalizedData
from dashboard.models import CustomAPI

def populate():
    # 1. Create Demo User
    username = 'demo_dev'
    password = 'password123'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        print(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")

    # 2. Add External Accounts
    ExternalAccount.objects.get_or_create(
        user=user,
        provider='github',
        defaults={'access_token': 'gh_fake_token_for_demo'}
    )
    ExternalAccount.objects.get_or_create(
        user=user,
        provider='spotify',
        defaults={'access_token': 'sp_fake_token_for_demo'}
    )
    print("External accounts linked.")

    # 3. Add Normalized GitHub Data
    github_sample = {
        'repositories': [
            {'name': 'quantum-core', 'stars': 124, 'language': 'Python', 'description': 'Quantum simulation engine', 'url': 'https://github.com/demo/quantum'},
            {'name': 'neural-visualizer', 'stars': 89, 'language': 'TypeScript', 'description': '3D Neural network visualizer', 'url': 'https://github.com/demo/neural'},
            {'name': 'api-guard', 'stars': 45, 'language': 'Go', 'description': 'Cloud-native API gateway', 'url': 'https://github.com/demo/guard'},
            {'name': 'rust-analyzer-plus', 'stars': 210, 'language': 'Rust', 'description': 'Enhanced analysis for Rust', 'url': 'https://github.com/demo/rust'},
            {'name': 'web-frame', 'stars': 67, 'language': 'JavaScript', 'description': 'Lightweight web framework', 'url': 'https://github.com/demo/web'},
            {'name': 'data-miner', 'stars': 34, 'language': 'Python', 'description': 'Data extraction tools', 'url': 'https://github.com/demo/miner'},
        ]
    }
    NormalizedData.objects.update_or_create(
        user=user,
        source='github',
        defaults={'data': github_sample}
    )

    # 4. Add Normalized Spotify Data
    spotify_sample = {
        'playlists': [
            {'name': 'Deep Focus', 'tracks': 56},
            {'name': 'Techno 2026', 'tracks': 120},
            {'name': 'Developer Chill', 'tracks': 85}
        ],
        'top_tracks': ['Synthesis', 'Logic Gate', 'Circuit Breaker']
    }
    NormalizedData.objects.update_or_create(
        user=user,
        source='spotify',
        defaults={'data': spotify_sample}
    )
    print("Normalized data populated.")

    # 5. Add Custom APIs
    CustomAPI.objects.update_or_create(
        user=user,
        endpoint_name='project-summary',
        defaults={'config': {'source': 'github', 'fields': ['name', 'language']}}
    )
    CustomAPI.objects.update_or_create(
        user=user,
        endpoint_name='music-vibe',
        defaults={'config': {'source': 'spotify', 'fields': ['top_tracks']}}
    )
    print("Custom API projections created.")

    print("\n" + "="*30)
    print("SAMPLE DATA POPULATION COMPLETE")
    print(f"Login Username: {username}")
    print(f"Login Password: {password}")
    print("="*30)

if __name__ == '__main__':
    populate()
