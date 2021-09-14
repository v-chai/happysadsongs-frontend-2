import requests
from api.keys import model_base_url

def PredictTop(list):
    for song in list.values():
        tmp = song['Lyrics']
        if len(tmp) < 20:
            continue
        r = requests.get(f'{model_base_url}{tmp[:1500]}')
        print(r)
        print(r.json())
    return None
