import requests
from api.keys import model_base_url
from statistics import mode, mean

def PredictTop(list):
    checked_songs = []
    preds = []
    valence = []
    for song in list.values():
        tmp = song['Lyrics']
        if len(tmp) < 20 or song['Language'] != "en":
            continue
        r = requests.get(f'{model_base_url}', params={'lyric': tmp[:1500]})
        if r.status_code == 200:
            preds.append(r.json()['prediction'])
            checked_songs.append(f"{song['Artist Names'][0]} - {song['Song Name']}")
            valence.append(float(song["Valence"]))
        else:
            continue
    try:
        overall_pred = int(mode(preds))
    except:
        overall_pred = 1
    avg_valence = mean(valence)

    return checked_songs, overall_pred, avg_valence
