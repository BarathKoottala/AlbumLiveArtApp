from dotenv import load_dotenv
load_dotenv()  # load SPOTIFY_* from a .env file (if present) before music reads env

from flask import Flask, render_template, request, make_response, jsonify
from functools import wraps
from music import get_music
from threading import Thread
import globals
import logging

current_song = ""
current_album = ""
current_artist = ""


app = Flask(__name__, static_url_path='/static')

def set_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
    return decorated_function


@app.route('/turnOnLights')
def light_up():
    message = "Turning on Lights"
    return jsonify({'message': message})


@app.route("/health")
def health():
    return "OK", 200


@app.route("/healthcheck")
def healthcheck():
    return "OK", 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPalette', methods=['GET'])
def get_palette():
    """API endpoint to return the extracted color palette."""
    if globals.global_palette is None:
        return jsonify({"palette":[[255, 255, 255]]})
    else:
        return jsonify({"palette": globals.global_palette})

@app.route('/nowPlaying', methods=['GET'])
def now_playing():
    """Everything the frontend needs in one poll: track text, palette, tempo
    (BPM) for the spin speed, and playback progress for the progress bar."""
    return jsonify(globals.now_playing)

if __name__ == '__main__':
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    # Single worker: polls Spotify, draws the vinyl, and computes the palette +
    # BPM event-driven whenever the song changes (see music.get_track).
    t1 = Thread(target=get_music, daemon=True)
    t1.start()
    app.run(port=8080, debug=True, use_reloader=False)