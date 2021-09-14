import requests
from api.keys import model_base_url

def PredictTop(list):
    print("_________________ PREDICT STARTED _________________")
    for song in list.values():
        tmp = song['Lyrics']
        print(tmp)
        if len(tmp) < 20 or song['Language'] is not 'en':
            continue
        r = requests.get(f'{model_base_url}{tmp[:1500]}')
        if r.status_code == 200:
            print(r.json())
        else:
            print(song)
    return None
