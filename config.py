import json
from gmusicapi import Mobileclient
import os
CONFIG_FILE_NAME = 'gmusic2mp3.json'

def print_all_my_devices(api: Mobileclient):
    for device in api.get_registered_devices():
        print('{')
        for k in device:
            print('\t{}: {}'.format(k, device[k]))
        print('}')

def generate_config():
    CONFIG = {
        'login': 'music_fun@gmail.com',
        'password': 'Bu!He8ePH0',
        'device_id': '39c5fb55f84a1d9a',
        'root_dir': r'C:\Users\nikol\GMusic',
        'albums': {
            'Несчастный случай': ['Чернослив и курага', ],
            'System Of A Down': ['Mezmerize', ]
        }
    }
    json.dump(CONFIG, open(CONFIG_FILE_NAME, 'w', encoding='utf8'), indent=2, ensure_ascii=False)


if not os.path.exists(CONFIG_FILE_NAME):
    generate_config()
    raise AssertionError('Cannot find config file. But, for example, generated the new one; please edit it :)')

CONFIG = json.load(open(CONFIG_FILE_NAME, 'r', encoding='utf8'))
