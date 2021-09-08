import lyricsgenius
from api.keys import genius_auth_token
import base64

genius = lyricsgenius.Genius(genius_auth_token)

def GetLyricsFromName(name):
    tmp = genius.search_song(title=base64.b64decode(name).decode())
    if tmp is not None:
        return {'lyric':tmp.lyrics}
    else:
        return {'lyric': ''}


def GetLyricsFromCustom(custom):
    if isinstance(custom[0], str):
        del custom[0]
    for idx, song in custom.items():
        print(song)
        art = song['Artist Names'][0]
        name = song['Song Name']
        tmp = genius.search_song(f'{name} {art}')
        if tmp is not None:
            song['Lyrics'] = tmp.lyrics
    return custom
