from typing import Any, Dict, List, Union
from core.normalizers.base import BaseNormalizer

class GitHubNormalizer(BaseNormalizer):
    """
    Normalizer for GitHub API data.
    """

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a single GitHub repository object.
        """
        return {
            'external_id': str(raw_data.get('id')),
            'name': raw_data.get('name'),
            'full_name': raw_data.get('full_name'),
            'description': raw_data.get('description'),
            'url': raw_data.get('html_url'),
            'language': raw_data.get('language'),
            'stars': raw_data.get('stargazers_count', 0),
            'forks': raw_data.get('forks_count', 0),
            'source': 'github',
            'metadata': {
                'owner': raw_data.get('owner', {}).get('login'),
                'created_at': raw_data.get('created_at'),
                'updated_at': raw_data.get('updated_at'),
                'is_private': raw_data.get('private', False),
            }
        }
