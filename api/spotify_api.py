import requests
import base64
from api.keys import spotify_id, spotify_sect, return_url, base_url

spotify_scope = "user-read-recently-played"


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

def GetTracksSpecs(token, response):
    r = requests.get(
        'https://api.spotify.com/v1/audio-features',
        headers={'Authorization': f"Bearer {token['access_token']}"},
        params={'ids': response[0]})
    specs = r.json()
    for idx, tracks in enumerate(specs['audio_features']):
        tracks['Song Name'] = response[idx+1]["Song Name"]
    return specs


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
