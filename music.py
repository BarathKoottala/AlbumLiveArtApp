#!/usr/local/bin/python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
import requests
from auth import *
import spotipy.util as util
from artwork import draw_record_overlay
from color import compute_palette
import globals
import time
import logging
from logging.handlers import RotatingFileHandler
# from color import get_color_palette_min_batch

# Set up logging
logger = logging.getLogger('spotify_artwork_app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add rotating file handler
file_handler = RotatingFileHandler("example.log", maxBytes=5*1024*1024, backupCount=1)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Add console handler to see logs in terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

current_track_id = None
spotify_cli_client_id = os.environ.get('SPOTIFY_CLI_CLIENT_ID')
spotify_cli_client_secret = os.environ.get('SPOTIFY_CLI_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI')

# Spotify blocks audio-features (tempo) for newer apps, so BPM comes from the
# free GetSongBPM API instead. Get a key at https://getsongbpm.com/api
# (their TOS requires a visible backlink to getsongbpm.com — added in the page).
GETSONGBPM_API_KEY = os.environ.get('GETSONGBPM_API_KEY')

# Keep the token cache OUT of static/ (which is web-served) so the refresh
# token can't be downloaded over HTTP.
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache-barath")

CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player"

class Track():

    def __init__(self, album, item):
        self.album_name = album["name"]
        self.artists = album["artists"][0]["name"]
        self.album_art_url = album["images"][0]["url"]
        self.track_name = item["name"]
        self.duration = item["duration_ms"]
        self.track_id = item["id"]

def get_auth_manager():
    # SpotifyOAuth transparently refreshes the access token (using the cached
    # refresh token) before each request, so the app never gets stuck on an
    # expired token the way a static token string would.
    return SpotifyOAuth(
        client_id=spotify_cli_client_id,
        client_secret=spotify_cli_client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-currently-playing",
        cache_path=CACHE_PATH,
        open_browser=False,
    )

def fetch_tempo(artist, title):
    """Look up a song's tempo (BPM) via the GetSongBPM API. Returns a float or
    None (no key configured, no match, or request error)."""
    if not GETSONGBPM_API_KEY:
        return None
    try:
        params = {
            "api_key": GETSONGBPM_API_KEY,
            "type": "both",
            "lookup": f"song:{title} artist:{artist}",
        }
        results = requests.get("https://api.getsong.co/search/", params=params, timeout=8).json().get("search")
        # The API returns {"search": {"error": ...}} when nothing matches.
        if not results or isinstance(results, dict):
            return None
        first = results[0]
        if first.get("tempo"):
            return float(first["tempo"])
        # Search didn't include tempo -> fetch the full song record by id.
        song_id = first.get("id")
        if song_id:
            song = requests.get(
                "https://api.getsong.co/song/",
                params={"api_key": GETSONGBPM_API_KEY, "id": song_id},
                timeout=8,
            ).json().get("song", {})
            if song.get("tempo"):
                return float(song["tempo"])
    except Exception as e:
        logger.debug(f"GetSongBPM lookup failed: {e}")
    return None


def get_track(sp):
    try:
        results = sp.current_user_playing_track()
        if results is None or results.get("item") is None:
            print("No track currently playing")
            globals.now_playing["is_playing"] = False
            globals.now_playing["sampled_at"] = time.time()
            time.sleep(1)
            return

        item = results["item"]
        track = Track(album=item["album"], item=item)

        # --- always-fresh, lightweight state (for the progress bar) ---
        globals.now_playing.update({
            "track": track.track_name,
            "artist": track.artists,
            "album": track.album_name,
            "progress_ms": results.get("progress_ms") or 0,
            "duration_ms": track.duration,
            "is_playing": bool(results.get("is_playing")),
            "sampled_at": time.time(),
        })

        # --- song-change detection: only do the expensive work on change ---
        global current_track_id
        if current_track_id == track.track_id:
            print("Same song, refreshing progress only")
            time.sleep(1)
            return
        current_track_id = track.track_id

        print(f'Currently Playing: {track.track_name} by {track.artists}\n')
        logger.debug("Making album image request")

        # New song -> download art and redraw the vinyl composite.
        img_data = requests.get(track.album_art_url).content
        with open('./static/album_art.jpg', 'wb') as handler:
            handler.write(img_data)
        draw_record_overlay("./static/record.png", "./static/album_art.jpg", "./static/vinyl.png")

        # New song -> recompute palette once (event-driven, fast & local).
        try:
            palette = compute_palette("./static/album_art.jpg", 5)
            globals.global_palette = palette
            globals.now_playing["palette"] = palette
        except Exception as e:
            logger.debug(f"Palette computation failed: {e}")

        # Art + palette are ready -> let the frontend crossfade NOW, BEFORE the
        # (networked, possibly slow) BPM lookup. Otherwise a manual skip waits on
        # GetSongBPM's response before the artwork changes — the inconsistent lag.
        globals.now_playing["art_version"] += 1

        # Tempo only affects spin speed; it can arrive a poll later.
        tempo = fetch_tempo(track.artists, track.track_name)
        logger.debug(f"Tempo for '{track.track_name}': {tempo}")
        globals.now_playing["tempo"] = tempo
        time.sleep(1)
    except requests.exceptions.ReadTimeout as e:
        print(str(e))
        time.sleep(3)
    except spotipy.SpotifyException as e:
        logger.debug(f"Spotify API error: {e}")
        time.sleep(3)


def get_music():
    print("Starting")
    print("Spotify Artwork App")
    # The auth_manager refreshes the token automatically on every request, so
    # there's no manual expiry timer to get out of sync with the real token.
    sp = spotipy.Spotify(auth_manager=get_auth_manager())
    while True:
        get_track(sp)

# if __name__ == "__main__":
#     logger.debug("Running main")

# main()
# get_music()  # don't run the infinite Spotify-poll loop on import; app.py starts it in a thread