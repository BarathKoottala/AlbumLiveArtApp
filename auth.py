import requests
import os
import sys
import time
import base64
import datetime, timedelta

class colors:
    GREEN='\033[92m'

future_expiry_time = 0

def get_auth_token():
    headers = {}
    data = {}
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_CLI_CLIENT_ID = os.environ.get('SPOTIFY_CLI_CLIENT_ID')
    SPOTIFY_CLI_CLIENT_SECRET = os.environ.get('SPOTIFY_CLI_CLIENT_SECRET')
    message = f"{SPOTIFY_CLI_CLIENT_ID}:{SPOTIFY_CLI_CLIENT_SECRET}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"
    r = requests.post(TOKEN_URL, headers=headers, data=data)
    json_response = r.json()
    print(json_response)
    expires_in = json_response['expires_in']
    hours = expires_in/60
    future_expiry_time = datetime.datetime.now() + datetime.timedelta(hours=hours)
    token = json_response['access_token']
    return token

def display_progress():
    count = 1
    for count in range(100):
        time.sleep(0.1)
        count+=1
        if count % 4 == 0:
            sys.stdout.write(f'{colors.GREEN}|')
            sys.stdout.flush()
            sys.stdout.write('\b')
        elif count % 4 == 1:
            sys.stdout.write(f'{colors.GREEN}/')
            sys.stdout.flush()
            sys.stdout.write('\b')
        elif count % 4 == 2:
            sys.stdout.write(f'{colors.GREEN}-')
            sys.stdout.flush()
            sys.stdout.write('\b')
        else:
            sys.stdout.write(f'{colors.GREEN}\\')
            sys.stdout.flush()
            sys.stdout.write('\b')
    
# display_progress()
get_auth_token()