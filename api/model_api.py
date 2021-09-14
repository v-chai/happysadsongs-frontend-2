import requests
from api.keys import model_base_url

def PredictTop(list):
    for song in list.values():
        tmp = song['Lyrics']
        r = requests.get(f'{model_base_url}{tmp}')
        print(r)
        print(r.json())
    return None
