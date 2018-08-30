from gmusicapi import Mobileclient
import wget
import os
from config import CONFIG

def main():
    api = Mobileclient()
    print('login as {} to Google Music...'.format(CONFIG['login']))
    if api.login(CONFIG['login'], CONFIG['password'], CONFIG['device_id']):
        if not api.is_subscribed:
            raise AssertionError('You has not Google Music subscription :(')

        print('Reading all songs...')
        lib = api.get_all_songs()
        albums = CONFIG['albums']
        for artist in albums:
            print('Artist: {}'.format(artist))
            for album in albums[artist]:
                print('Album: {}'.format(album))
                tracks = sorted([t for t in lib if t['album'] == album and t['artist'] == artist], key=lambda t: t['trackNumber'])
                if tracks:
                    dir_name = os.path.join(CONFIG['root_dir'], artist, "{} {}".format(tracks[0]['year'], album))
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                    for tr in tracks:
                        if 'albumArtRef' in tr:
                            i = 0
                            for artRef in tr['albumArtRef']:
                                img_file_name = 'cover.{}.jpg' if i else 'cover.jpg'
                                full_path = os.path.join(dir_name, img_file_name)
                                if not os.path.exists(full_path):
                                    wget.download(artRef['url'], full_path)
                        url = api.get_stream_url(tr['id'])
                        file_name = '{:02d} {}.mp3'.format(tr['trackNumber'], tr['title'])
                        file_name = file_name.replace('/', '-')
                        file_name = file_name.replace('"', '-')
                        full_path = os.path.join(dir_name, file_name)
                        if not os.path.exists(full_path):
                            wget.download(url, full_path)
        api.logout()


if __name__ == "__main__":
    # execute only if run as a script
    main()
