import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from PIL import Image
import requests
from io import BytesIO
from auth import get_auth_token

def get_artwork(album_id):
    # sp = spotipy.Spotify(auth=token)
    # album = "Her Loss"
    # results = sp.search(id= q = "album:" + album, type = "album")
    # album_id = results['albums']['items'][0]['uri']
    # print(results)
    token = get_auth_token()
    parameters = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + token,
        "Host": "api.spotify.com",
    }
    print("album_id is: " + album_id)
    album_url = "https://api.spotify.com/v1/albums/" + album_id
    response = requests.get(album_url, params=parameters)
    print(response.json)
    return response
    # img = Image.open(BytesIO(response.content))

#TODO: Attempt to make function that makes the album artwork resemble a record spinning
def make_artwork_spin():
    pass