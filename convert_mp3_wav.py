import os
import sys

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

import os_tools


# convert all songs to wav files
def __convert_files(album_path):
    album_mp3_path = os.path.join(album_path, 'mp3')
    album_wav_path = os.path.join(album_path, 'wav')
    os_tools.reset_dir(album_wav_path)

    mp3_files = os.listdir(album_mp3_path)

    for mp3_file_name in mp3_files:

        mp3_file = os.path.join(album_mp3_path, mp3_file_name)
        pre, ext = os.path.splitext(mp3_file)
        if ext == '.mp3':
            wav_file = os.path.join(album_wav_path, os.path.basename(pre) + '.wav')

            try:
                sound = AudioSegment.from_mp3(mp3_file)
                sound.export(wav_file, format='wav')
            except CouldntDecodeError:
                print('not convertible ' + mp3_file)
            except IndexError:
                print('not a mp3 file ' + mp3_file)


# detect the current working directory and print it
current_path = os.getcwd()


def convert_all():
    # get my dir
    data_dir = os.path.join(os.getcwd(), 'data')

    # walk the data directory and convert all mp3
    for album in os.listdir(data_dir):
        album_path = os.path.join(data_dir, album)

        # convert every album
        __convert_files(album_path)


convert_all()

sys.exit(0)
