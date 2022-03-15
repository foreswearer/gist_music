
import os
import shutil

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


# convert all songs to wav files
def convert_files(mp3_dir, wav_dir):

    audio_paths = os.listdir(mp3_dir)

    # make the top level directory
    try:
        shutil.rmtree(wav_dir)
    except OSError:
        pass
    try:
        os.mkdir(wav_dir)
    except OSError:
        pass

    for song in audio_paths:

        song = os.path.join(mp3_dir, song)
        pre, ext = os.path.splitext(song)
        wav_song = os.path.join(wav_dir, os.path.basename(pre) + '.wav')

        try:
            sound = AudioSegment.from_mp3(song)
            sound.export(wav_song, format="wav")
        except CouldntDecodeError:
            print ('not convertible ' + song)
        except IndexError:
            print ('problem with index ' + song)

# detect the current working directory and print it
current_path = os.getcwd()
print ("The current working directory is %s" % current_path)

# walk the data directory and convert all mp3
for rootdir, dirs, files in os.walk(os.path.join(current_path, 'data')):
    for album_path in dirs:
        if album_path != 'wav':
            album_path = os.path.join(rootdir, album_path)
            album_wav_path = os.path.join(album_path, 'wav')
            # convert every album
            convert_files(album_path, album_wav_path)
