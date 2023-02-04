#!/usr/local/bin/python
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'svg'
from skimage import io as imgio
from skimage.transform import resize
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import requests
from auth import *
import spotipy.util as util
from artwork import get_artwork
import pyfiglet 



CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player"

def get_track():
    result = pyfiglet.figlet_format("Spotify Artwork App") 
    # print(result)
    sys.stdout.write(f'{colors.GREEN}{result}')
    # If authentication error occurs, most likely have to source ~/.bash-profile again
    # You can automate this process by adding source ~/.bash-profile to 
    # your ~/.bash_profile
    spotify_cli_client_id = os.environ.get('SPOTIFY_CLI_CLIENT_ID')
    spotify_cli_client_secret = os.environ.get('SPOTIFY_CLI_CLIENT_SECRET')
    username = "barath"
    scope = "user-read-currently-playing"
    redirect_uri = os.environ.get('redirect_uri')
    token = util.prompt_for_user_token(username, scope, spotify_cli_client_id, spotify_cli_client_secret, redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playing_track()
        item = results["item"]
        album = item["album"]
        track = album["name"]
        artists = album["artists"]
        track_id = item["id"] # TODO: Eventually want to continuously check next song is the same as the current song
        artists_name = ', '.join(artist['name'] for artist in artists)
        sys.stdout.write(f'{colors.GREEN}Currently Playing: {track} by {artists_name}\n')
    else:
        print("Can't get token for", username)
    
    print("Making album image request")
    album_art_url = album["images"][0]["url"]
    img_data = requests.get(album_art_url).content
    with open('album_art.jpg', 'wb') as handler:
        handler.write(img_data)
    

get_track()
