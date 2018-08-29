from gmusicapi import Mobileclient
import wget
import os
import json

CONFIG_FILE_NAME = 'gmusic2mp3.json'

def print_all_my_devices(api: Mobileclient):
    for device in api.get_registered_devices():
        print('{')
        for k in device:
            print('\t{}: {}'.format(k, device[k]))
        print('}')

def generate_config():
    CONFIG = {
                'login': 'nchernov@gmail.com',
                'password': 'Bu!He8ePH0',
                'device_id': '39c5fb55f84a1d9a',
                'root_dir': r'C:\Users\nikol\GMusic',
                'albums': {
                    'Несчастный случай': 'Чернослив и курага',
                    'System Of A Down': 'Mezmerize'
                }
             }
    with open(CONFIG_FILE_NAME, 'w', encoding='utf8') as f:
        json.dump(CONFIG, f, indent=2, ensure_ascii=False)


def main():
    CONFIG = None
    if not os.path.exists(CONFIG_FILE_NAME):
        generate_config()
        raise AssertionError('Cannot find config file. But, for example, generated the new one; please edit it :)')
    with open(CONFIG_FILE_NAME, 'r') as f:
        CONFIG = json.load(open(CONFIG_FILE_NAME))
    api = Mobileclient()
    if api.login(CONFIG['login'], CONFIG['password'], CONFIG['device_id']):
        if not api.is_subscribed:
            raise AssertionError('You has not Google Music subscription :(')

        lib = api.get_all_songs()
        albums = CONFIG['albums']
        for artis in albums:
            album = albums[artis]
            tracks = sorted([t for t in lib if t['album'] == album and t['artist'] == artis], key=lambda t: t['trackNumber'])
            if tracks:
                dir_name = os.path.join(CONFIG['root_dir'], artis, "{} {}".format(tracks[0]['year'], album))
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                for tr in tracks:
                    url = api.get_stream_url(tr['id'])
                    file_name = '{:02d} {}.mp3'.format( tr['trackNumber'], tr['title'])
                    file_name = file_name.replace('/', '-')
                    full_path = os.path.join(dir_name, file_name)
                    if not os.path.exists(full_path):
                        wget.download(url, full_path)


if __name__ == "__main__":
    # execute only if run as a script
    main()