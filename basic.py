#!/usr/local/bin/python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import requests
from auth import *
import spotipy.util as util
from artwork import get_artwork
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('spotify_artwork_app')
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
handler = RotatingFileHandler("example.log", maxBytes=5*1024*1024, backupCount=1)
logger.addHandler(handler)


current_track_id = None
spotify_cli_client_id = os.environ.get('SPOTIFY_CLI_CLIENT_ID')
spotify_cli_client_secret = os.environ.get('SPOTIFY_CLI_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI')

CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player"

def get_track():
   
    # If authentication error occurs, most likely have to source ~/.bash-profile again
    # You can automate this process by adding source ~/.bash-profile to 
    # your ~/.bash_profile
    
    username = "barath"
    scope = "user-read-currently-playing"
    global logger
    logger.info(redirect_uri)
    token = util.prompt_for_user_token(username, scope, spotify_cli_client_id, spotify_cli_client_secret, redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playing_track()
        if results == None:
            logger.info("No track currently playing")
            time.sleep(3)
            return
        item = results["item"]
        album = item["album"]
        album_name = album["name"]
        track_name = item["name"]
        artists = album["artists"]
        track_id = item["id"]
        global current_track_id
        if current_track_id == None or current_track_id != track_id:
            current_track_id = track_id
        elif current_track_id == track_id:
            logger.info("Same song, going to request later")
            time.sleep(1)
            return
        artists_name = ', '.join(artist['name'] for artist in artists)
        logger.info(f'{colors.GREEN}Currently Playing: {track_name} by {artists_name}\n')
    else:
        logger.info("Can't get token for", username)
    
    logger.info("Making album image request")
    album_art_url = album["images"][0]["url"]
    img_data = requests.get(album_art_url).content
    with open('./static/album_art.jpg', 'wb') as handler:
        handler.write(img_data)
        handler.close()
    time.sleep(1)
    

def main():
    logger.info("Starting")
    title = "Spotify Artwork App"
    logger.info(f'{colors.GREEN}{title}')
    while(True):
        get_track()

if __name__ == "__main__":
    logger.info("Starting")
    