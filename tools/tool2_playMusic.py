import webbrowser
from langchain.tools import tool
from typing import Optional
@tool
def play_spotify_music(query: Optional[str] = "") ->dict:
    if not query:
        return "No song selected"
    """
    Opens Spotify with the given search query or Spotify URL.
    Example inputs:
        - "lofi chill"
        - "https://open.spotify.com/track/XYZ"
        - "lofi beats playlist"
    """
    # If user passed a URL, open directly
    if query.startswith("http"):
        webbrowser.open(query)
        return {"status": "success", "action": "opened_url", "query": query}

    # Otherwise open search page
    search_url = "https://open.spotify.com/search/" + query.replace(" ", "%20")
    webbrowser.open(search_url)
    return {"status": "success", "action": "opened_search", "query": query}


# play_spotify_music("Oh Khuda")
