from langchain.tools import tool
from typing import Optional

@tool
def play_spotify_music(query: Optional[str] = "") -> dict:
    """
    Returns a Spotify search URL for the given song.
    """
    if not query:
        return {"status": "error"}

    url = "https://open.spotify.com/search/" + query.replace(" ", "%20")
    print(url)
    return {
        "status": "success",
        "song": query,
        "url": url
    }

