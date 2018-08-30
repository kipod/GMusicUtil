import json
from gmusicapi import Mobileclient
from config import CONFIG, CONFIG_FILE_NAME

def main():
    api = Mobileclient()
    print('login as {} to Google Music...'.format(CONFIG['login']))
    if api.login(CONFIG['login'], CONFIG['password'], CONFIG['device_id']):
        if not api.is_subscribed:
            raise AssertionError('You has not Google Music subscription :(')

        lib = api.get_all_songs()
        print('Reading all songs...')
        artist_album = {}
        for tr in lib:
            artist = tr['artist']
            album = tr['album']
            if artist not in artist_album:
                artist_album[artist] = [album, ]
            if album not in artist_album[artist]:
                artist_album[artist] += [album, ]

        CONFIG['albums'] = artist_album
        json.dump(CONFIG, open(CONFIG_FILE_NAME, 'w', encoding='utf8'), indent=2, ensure_ascii=False)
        api.logout()


if __name__ == "__main__":
    # execute only if run as a script
    main()
