from typing import List, Dict, Any

def normalize_github_data(raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalizes raw GitHub repository data into a structured summary.
    
    Expected Output Format:
    {
        "repo_count": int,
        "repos": [
            {
                "name": str,
                "url": str,
                "stars": int,
                "language": str
            },
            ...
        ],
        "languages": {
            "Python": int,
            "JavaScript": int,
            ...
        }
    }
    """
    repos_list = []
    languages_stats = {}
    
    for repo in raw_data:
        # Extract individual repo info
        repo_info = {
            "name": repo.get("name"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language")
        }
        repos_list.append(repo_info)
        
        # Calculate language statistics
        lang = repo.get("language")
        if lang:
            languages_stats[lang] = languages_stats.get(lang, 0) + 1
            
    normalized_result = {
        "repo_count": len(repos_list),
        "repos": repos_list,
        "languages": languages_stats
    }
    
    return normalized_result

def normalize_spotify_data(playlists_raw: List[Dict[str, Any]], artists_raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalizes raw Spotify data into a structured summary.
    """
    playlists = []
    for p in playlists_raw:
        playlists.append({
            "name": p.get("name"),
            "url": p.get("external_urls", {}).get("spotify"),
            "tracks_count": p.get("tracks", {}).get("total", 0)
        })

    artists = []
    genre_stats = {}
    for a in artists_raw:
        genres = a.get("genres", [])
        artists.append({
            "name": a.get("name"),
            "genres": genres
        })
        for g in genres:
            genre_stats[g] = genre_stats.get(g, 0) + 1

    return {
        "playlist_count": len(playlists),
        "playlists": playlists,
        "top_artists": artists,
        "genres": genre_stats
    }
