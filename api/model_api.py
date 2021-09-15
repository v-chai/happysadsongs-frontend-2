import requests
from api.keys import model_base_url
from statistics import mode, mean

def PredictTop(list):
    checked_songs = []
    preds = []
    valence = []
    backup_valence = []
    for song in list.values():
        tmp = song['Lyrics']
        if len(tmp) < 20 or song['Language'] != "en":
            continue
        r = requests.get(f'{model_base_url}', params={'lyric': tmp[:1500]})
        if r.status_code == 200:
            preds.append(int(r.json()['prediction']))
            checked_songs.append(f"{song['Artist Names'][0]} - {song['Song Name']}")
            valence.append(float(song["Valence"]))
            backup_valence.append(float(song["Valence"]))
        else:
            backup_valence.append(float(song["Valence"]))
    if len(checked_songs) > 0:
        try:
            overall_pred = mode(preds)
        except:
            overall_pred = 2
        avg_valence = mean(valence)
        sad_count = preds.count(1)
        happy_count = preds.count(0)
    else:
        avg_valence = mean(backup_valence)
        overall_pred = "Could not analyze any lyrics."
        sad_count = 0
        happy_count = 0
    return checked_songs, overall_pred, avg_valence, sad_count, happy_count
