import requests
from api.keys import model_base_url

def PredictTop(list):
    print("_________________ PREDICT STARTED _________________")
    for song in list.values():
        tmp = song['Lyrics']
        if len(tmp) < 20 or song['Language'] != "en":
            continue
        r = requests.get(f'{model_base_url}', params={'lyric', tmp[:1500]})
        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(song)
    return None
