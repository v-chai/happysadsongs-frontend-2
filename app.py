from re import template
from flask import Flask, redirect, url_for, session, request
import urllib.parse
from datetime import timedelta

import requests

from api.keys import spotify_id, return_url
from api.spotify_api import GenToken, GetCustomList
from api.xmatch_api import GetLyricsFromCustom, GetLyricsFromName

app = Flask(__name__)
app.secret_key = 'spotify_secret'
app.permanent_session_lifetime = timedelta(minutes=5)

spotify_scope = "user-read-recently-played"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    parms = {'client_id':spotify_id, 'redirect_uri':return_url, 'response_type':'code', 'scope':spotify_scope}
    parm = urllib.parse.urlencode(parms)
    return redirect(
        f'https://accounts.spotify.com/authorize?{parm}'
    )


@app.route('/login/authorized')
def spotify_authorized():
    session['token'] = GenToken(request.args.get('code')).json()
    return redirect(url_for('listplayed'))


@app.route('/listplayed')
def listplayed():
    session.permanent = True
    return GetCustomList(session['token'])


@app.route('/lyrics')
def lyrics():
    return GetLyricsFromName(request.args.get('name'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4006)
