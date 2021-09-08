import requests
import base64
from urllib.parse import urlencode
from api.keys import spotify_id, spotify_sect, return_url

spotify_scope = "user-read-recently-played"


def GetRecentPlayed(token):
    r = requests.get('https://api.spotify.com/v1/me/player/recently-played',
                     headers={'Authorization': f"Bearer {token}", 'limit':'10'})
    return r.json()


def GetCustomList(token):
    played_list = GetRecentPlayed(token['access_token'])
    cust_list = {}
    for idx, tracks in enumerate(played_list['items']):
        artist = []
        for art in tracks['track']['artists']:
            artist.append(art['name'])

        name = tracks['track']['name']
        pop = tracks['track']['popularity']
        duration = tracks['track']['duration_ms']
        preview = tracks['track']['preview_url']

        first_art = artist[0]
        comp = f'{name} {first_art}'
        lyrics = f'http://187.57.39.163:4006/lyrics?name={base64.b64encode(comp.encode()).decode()}'

        cust_list[idx] = {
            "Song Name": name,
            "Artist Names": artist,
            "Popularity": pop,
            "Duration": duration / 1000,
            "Preview": preview,
            "Lyrics": lyrics
        }
    return cust_list


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
