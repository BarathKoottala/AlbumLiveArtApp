import requests
import os
import sys
import time
import base64

class colors:
    GREEN='\033[92m'

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
    print(r.json())
    token = r.json()['access_token']
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
#get_auth_token()