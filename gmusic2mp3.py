''' Download mp3 files from Google Music Library '''
import os

import wget
from gmusicapi import Mobileclient
from mp3_tagger import VERSION_1, VERSION_2, MP3File
from mp3_tagger.genres import GENRES

from config import CONFIG


def str_utf8(value: str) -> str:
    result = value.replace('\u2019', "'")
    result = result.encode('utf-8').decode('utf-8')
    return result


def fix_path_name(file_name):
    result = file_name.replace('/', '-')
    result = result.replace('?', '.')
    result = result.replace('`', '\'')
    return result


def fix_file_name(file_name):
    result = fix_path_name(file_name)
    result = result.replace(':', '-')
    result = result.replace('"', '-')
    result = result.replace('(', '\'')
    result = result.replace(')', '\'')
    return result


def update_tags(track: map, path_mp3: str):
    # Create MP3File instance.
    mp3 = MP3File(path_mp3)
    # Get all tags.
    tags = None
    try:
        tags = mp3.get_tags()
    except UnicodeDecodeError:
        pass
    if tags and 'ID3TagV1' not in tags:
        tags = None
    elif tags and 'ID3TagV2' not in tags:
        tags = None
    elif tags and 'album' not in tags['ID3TagV1']:
        tags = None
    elif tags and 'album' not in tags['ID3TagV2']:
        tags = None
    elif tags and tags['ID3TagV1']['album'] is None:
        tags = None
    elif tags and tags['ID3TagV2']['album'] is None:
        tags = None
    if not tags or not (tags['ID3TagV1']['album'] in tags['ID3TagV2']['album']):
        title = str_utf8(track['title'])
        genre = str_utf8(track['genre'])
        album = str_utf8(track['album'])
        artist = str_utf8(track['artist'])
        composer = str_utf8(track['composer'])
        print('  fix tags for track: {}'.format(title))

        for _ in range(2):
            mp3 = MP3File(path_mp3)
            mp3.set_version(VERSION_1)
            mp3.album = album
            mp3.artist = artist
            mp3.year = str(track['year'])
            mp3.composer = composer
            try:
                for gen_idx in range(len(GENRES)):
                    if GENRES[gen_idx] in genre:
                        mp3.set_version(VERSION_1)
                        mp3.genre = gen_idx
                        break
            except UnicodeEncodeError:
                pass
            mp3.song = title
            mp3.track = str(track['trackNumber'])
            mp3.save()

            mp3 = MP3File(path_mp3)
            mp3.set_version(VERSION_2)
            mp3.album = album
            mp3.artist = artist
            mp3.year = str(track['year'])
            mp3.composer = composer
            try:
                mp3.genre = genre
            except UnicodeEncodeError:
                pass
            mp3.song = title
            mp3.track = str(track['trackNumber'])
            mp3.save()
    pass


def main():
    api = Mobileclient()
    print('login as {} to Google Music...'.format(CONFIG['login']))
    if api.login(CONFIG['login'], CONFIG['password'], CONFIG['device_id']):
        try:
            if not api.is_subscribed:
                raise AssertionError('You has not Google Music subscription :(')

            print('Reading all songs...')
            lib = api.get_all_songs()
            albums = CONFIG['albums']
            for artist in albums:
                print('Artist: {}'.format(artist))
                for album in albums[artist]:
                    print('Album: {}'.format(album))
                    tracks = sorted([t for t in lib if t['album'] == album and t['artist'] == artist],
                                    key=lambda t: t['trackNumber'])
                    if tracks:
                        dir_name = os.path.join(CONFIG['root_dir'], fix_file_name(artist), "{} {}".format(tracks[0]['year'], fix_file_name(album)))
                        if not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        for tr in tracks:
                            if 'albumArtRef' in tr:
                                i = 0
                                for artRef in tr['albumArtRef']:
                                    img_file_name = 'cover.{}.jpg' if i else 'cover.jpg'
                                    full_path = os.path.join(dir_name, img_file_name)
                                    full_path = fix_path_name(full_path)
                                    if not os.path.exists(full_path):
                                        wget.download(artRef['url'], full_path)
                            file_name = '{:02d} {}.mp3'.format(tr['trackNumber'], tr['title'])
                            file_name = fix_file_name(file_name)
                            full_path = os.path.join(dir_name, file_name)
                            if not os.path.exists(full_path):
                                url = api.get_stream_url(tr['id'])
                                wget.download(url, full_path)
                                update_tags(tr, full_path)
        finally:
            api.logout()


if __name__ == "__main__":
    # execute only if run as a script
    main()
