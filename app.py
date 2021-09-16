from flask import Flask, redirect, url_for, session, request, render_template
from flask_session import Session
from datetime import timedelta
from time import sleep

import os
import redis
from rq import Queue
from rq.job import Job

from api.spotify_api import GenToken, GetCustomList, GetTracksSpecs, GetCode, CategoryPlaylist, GetFeaturedPlaylists, GetFeatItems
from api.xmatch_api import GetLyricsFromCustom, GetLyricsFromName
from api.model_api import PredictTop

app = Flask(__name__)
app.secret_key = 'spotify_secret'
app.permanent_session_lifetime = timedelta(minutes=5)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


spotify_scope = "user-read-recently-played"


def internal_error(e):
    return redirect(url_for('home'))


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


@app.route('/getrecentsession')
def getrecentsession():
    session.permanent = True
    custom = GetCustomList(session['token'])
    session['songs'] = GetLyricsFromCustom(custom)
    print(session['songs'])
    return redirect(url_for('home'))


@app.route('/featuredplaylists')
def featuredplaylists():
    session.permanent = True
    feat = GetFeaturedPlaylists(session['token'])
    return GetFeatItems(session['token'], feat)



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
    session['running'] = 1
    return render_template('index.html')


@app.route('/api')
def api():
    return render_template('index_api.html')


@app.route('/anya')
def anya():
    if session['running'] == 1:
        session['song_list'] = listplayedfull()
        red = redis.from_url(os.environ.get("REDIS_URL"))
        q = Queue(connection=red)
        job = q.enqueue(PredictTop, session['song_list'])
        session['job_id'] = job.id
        session['running'] = 2
    red = redis.from_url(os.environ.get("REDIS_URL"))
    job = Job.fetch(session['job_id'], connection=red)
    if job.result == None:
        return render_template('intermediate.html',
                               value=job,
                               id=session['job_id'])
    session['running'] = 1
    return render_template('intermediate2.html',
                           value=job,
                           id=session['job_id'])


@app.route('/lyrics')
def lyrics():
    return GetLyricsFromName(request.args.get('name'))


if __name__ == "__main__":
    app.run()
