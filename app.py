from flask import Flask, render_template, request, url_for, make_response
from functools import wraps
from basic import main as get_music
from PIL import Image
from threading import Thread, Event
import base64
import io
import os

app = Flask(__name__, static_url_path='/static')

def set_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    t = Thread(target=get_music)
    t.start()
    app.run(debug=True)