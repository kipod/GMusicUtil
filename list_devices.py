import json
from gmusicapi import Mobileclient
from config import CONFIG, CONFIG_FILE_NAME

def print_all_my_devices(api: Mobileclient):
    for device in api.get_registered_devices():
        print('{')
        for k in device:
            print('\t{}: {}'.format(k, device[k]))
        print('}')

def main():
    api = Mobileclient()
    print('login as {} to Google Music...'.format(CONFIG['login']))
    if api.login(CONFIG['login'], CONFIG['password'], CONFIG['device_id']):
        if not api.is_subscribed:
            raise AssertionError('You has not Google Music subscription :(')

    print_all_my_devices(api)
    api.logout()


if __name__ == "__main__":
    # execute only if run as a script
    main()
