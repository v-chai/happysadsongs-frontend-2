from flask import Flask, redirect, url_for, session, request, render_template
from datetime import timedelta

from api.spotify_api import GenToken, GetCustomList, GetTracksSpecs, GetCode, CategoryPlaylist
from api.xmatch_api import GetLyricsFromCustom, GetLyricsFromName

app = Flask(__name__)
app.secret_key = 'spotify_secret'
app.permanent_session_lifetime = timedelta(minutes=5)

spotify_scope = "user-read-recently-played"


def internal_error(e):
    return redirect(url_for('home')), 400


app.register_error_handler(500, internal_error)


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/test')
def test():
    return CategoryPlaylist(session['token'], 'sad')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(GetCode())


@app.route('/login/authorized')
def spotify_authorized():
    session['token'] = GenToken(request.args.get('code')).json()
    return redirect(url_for('home'))


@app.route('/listplayed')
def listplayed():
    session.permanent = True
    return GetCustomList(session['token'])


@app.route('/listplayedlyrical')
def listplayedlyrical():
    session.permanent = True
    custom = GetCustomList(session['token'])
    return GetLyricsFromCustom(custom)


@app.route('/listplayedfeatures')
def listplayedfeatures():
    session.permanent = True
    custom = GetCustomList(session['token'])
    return GetTracksSpecs(session['token'], custom)


@app.route('/listplayedfull')
def listplayedfull():
    session.permanent = True
    custom = GetCustomList(session['token'])
    custom = GetTracksSpecs(session['token'], custom)
    return GetLyricsFromCustom(custom)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/api')
def home():
    return render_template('index_api.html')


@app.route('/lyrics')
def lyrics():
    return GetLyricsFromName(request.args.get('name'))


if __name__ == "__main__":
    app.run()
