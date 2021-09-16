import requests
import urllib
import base64
from api.keys import spotify_id, spotify_sect, return_url, base_url

spotify_scope = "user-read-recently-played"


def CategoryPlaylist(token, id):
    r = requests.get(
        f'https://api.spotify.com/v1/browse/categories/{id}/playlists',
        headers={'Authorization': f"Bearer {token['access_token']}"})
    return r.json()



def GetRecentPlayed(token):
    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=10',
                     headers={'Authorization': f"Bearer {token}"})
    return r.json()


def GetCustomList(token):
    played_list = GetRecentPlayed(token['access_token'])
    cust_list = {}
    id_list = []
    for idx, tracks in enumerate(played_list['items']):
        artist = []
        track = tracks['track']
        for art in track['artists']:
            artist.append(art['name'])

        name = track['name']
        pop = track['popularity']
        duration = track['duration_ms']
        preview = track['preview_url']
        id_list.append(track['id'])

        first_art = artist[0]
        comp = f'{name} {first_art}'
        lyrics = f'{base_url}/lyrics?name={base64.b64encode(comp.encode()).decode()}'

        cust_list[idx+1] = {
            "Song Name": name,
            "Artist Names": artist,
            "Popularity": pop,
            "Duration": duration / 1000,
            "Preview": preview,
            "Lyrics": lyrics
        }
    cust_list[0] = ','.join(id_list)
    return cust_list

def GetTracksSpecs(token, response, onlyval=False):
    r = requests.get(
        'https://api.spotify.com/v1/audio-features',
        headers={'Authorization': f"Bearer {token['access_token']}"},
        params={'ids': response})
    specs = {}
    if not onlyval:
        for idx, tracks in enumerate(r.json()['audio_features']):
            specs[idx] = {
                "Song Name": response[idx + 1]["Song Name"],
                "Artist Names": response[idx + 1]["Artist Names"],
                # "Danceability": tracks["danceability"],
                # "Duration": tracks["duration_ms"] / 1000,
                # "Energy": tracks["energy"],
                # "Liveness": tracks["liveness"],
                # "Loudness": tracks["loudness"],
                # "Mode": tracks["mode"],
                # "Tempo": tracks["tempo"],
                "Valence": tracks["valence"]
            }
    else:
        for idx, tracks in enumerate(r.json()['audio_features']):
            specs[idx] = {"Valence": tracks["valence"]}
    return specs

#Generate code used for token generation
def GetCode():
    parms = {
        'client_id': spotify_id,
        'redirect_uri': return_url,
        'response_type': 'code',
        'scope': spotify_scope
    }
    parm = urllib.parse.urlencode(parms)
    return f'https://accounts.spotify.com/authorize?{parm}'


#Generate token from given code
def GenToken(code):
    bod = {
        'grant_type':"authorization_code",
        'code': code,
        'redirect_uri': return_url
    }

    id_secrt = f'{spotify_id}:{spotify_sect}'
    head = {'Authorization': f'Basic {base64.b64encode(id_secrt.encode()).decode()}'}
    r = requests.post('https://accounts.spotify.com/api/token', data=bod, headers=head)
    return r


def GetFeaturedPlaylists(token):
    r = requests.get(
        'https://api.spotify.com/v1/browse/featured-playlists',
        headers={'Authorization': f"Bearer {token['access_token']}"})
    return r.json()


def GetFeatItems(token, feat):
    final = {}
    for idx, playlist in enumerate(feat['playlists']['items']):
        r = requests.get(
            playlist['tracks']['href'],
            headers={'Authorization': f"Bearer {token['access_token']}"})
        response = r.json()

        tracks = {}
        ids = []
        for idx_, track in enumerate(response['items']):
            ids.append(track['track']['id'])

        specs = GetTracksSpecs(token, ids, True)

        for idx__, track in enumerate(response['items']):
            print(idx__)
            tracks[idx__] = {
                "Song Name": track['track']['name'],
                "Artist Names": track['track']['artists'],
                "Valence": specs[idx__]['Valence']
            }
        final[idx] = {
            'playlist name':playlist['description'],
            'tracks':tracks
            }
    return final
