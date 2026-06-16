#!/usr/local/bin/python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import requests
from auth import *
import spotipy.util as util
from artwork import draw_record_overlay
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

CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player"
# CURRENT_COLOR = get_color_palette_min_batch("./static/album_art.jpg")

class Track():

    def __init__(self, album, item):
        self.album_name = album["name"]
        self.artists = album["artists"][0]["name"]
        self.album_art_url = album["images"][0]["url"]
        self.track_name = item["name"]
        self.duration = item["duration_ms"]
        self.track_id = item["id"]

def get_auth_token():
    username = "barath"
    scope = "user-read-currently-playing"
    global logger
    logger.debug(redirect_uri)
    token = util.prompt_for_user_token(username, scope, spotify_cli_client_id, spotify_cli_client_secret, redirect_uri)
    if token:
        logger.debug(f"Successfully fetched auth token: {str(token)}")
        return token
    else:
        logger.debug("Failed to fetch auth token")
        return None

def get_track(auth_token):
   
    # If authentication error occurs, most likely have to source ~/.bash-profile again
    # You can automate this process by adding source ~/.bash-profile to 
    # your ~/.bash_profile
    
    sp = spotipy.Spotify(auth=auth_token)
    try:
        results = sp.current_user_playing_track()
        if results == None:
            print("No track currently playing")
            time.sleep(1)
            return
        item = results["item"]
        track = Track(album=item["album"], item=results["item"])
        # album_name = album["name"]
        # track_name = item["name"]
        # duration = item["duration_ms"]
        # artists = album["artists"]
        # track_id = item["id"]
        global current_track_id
        if current_track_id == None or current_track_id != track.track_id:
            current_track_id = track.track_id
        elif current_track_id == track.track_id:
            print("Same song, going to request later")
            time.sleep(1)
            return
        artists_name = track.artists
        print(f'Currently Playing: {track.track_name} by {artists_name}\n')
    
        
        logger.debug("Making album image request")
        
        # album_art_url = album["images"][0]["url"]
        # img_data = requests.get(album_art_url).content
        img_data = requests.get(track.album_art_url).content
        with open('./static/album_art.jpg', 'wb') as handler:
            handler.write(img_data)
            handler.close()
            draw_record_overlay("./static/record.png", "./static/album_art.jpg", "./static/vinyl.png")
        time.sleep(1)
    except requests.exceptions.ReadTimeout as e:
        print(str(e))
        time.sleep(3)


def get_music():
    print("Starting")
    title = "Spotify Artwork App"
    print(f'{title}')
    token = get_auth_token()
    timeout = time.time() + 60*60 #60 minute timer (length of auth token)
    while(True):
        if token and time.time() < timeout:
            get_track(auth_token=token)
        else:
            token = get_auth_token()
            # timeout = time.time() + 60*60
            timeout = time.time() + 60

# if __name__ == "__main__":
#     logger.debug("Running main")

# main()
# get_music()  # don't run the infinite Spotify-poll loop on import; app.py starts it in a thread