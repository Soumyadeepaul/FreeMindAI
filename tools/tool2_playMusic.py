from langchain.tools import tool
from typing import Optional

@tool
def play_spotify_music(query: Optional[str] = "") -> dict:
    """
    Returns a Spotify URL for the given song or playlist.
    """

    if not query:
        return {
            "status": "error",
            "message": "No song selected"
        }

    # If already a Spotify URL
    if query.startswith("http"):
        url = query
    else:
        url = "https://open.spotify.com/search/" + query.replace(" ", "%20")

    return {
        "status": "success",
        "spotify_url": url,
        "message": f"Click the link to listen to {query}"
    }
