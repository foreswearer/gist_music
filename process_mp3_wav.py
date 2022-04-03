import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pyloudnorm as pyln
import seaborn as sns
import soundfile as sf
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

import os_tools

warnings.filterwarnings('ignore')

sns.set()
sns.set(rc={'figure.figsize': (12, 10)})


def __convert_mp3_to_wav(album_mp3_path, album_wav_path):
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


def __music_visualizations(album_wav_path, album_png_path):
    audio_paths = os.listdir(album_wav_path)

    # if the directory exists, delete it
    # then create a fresh one
    os_tools.reset_dir(album_png_path)

    for track in audio_paths:
        # set the track name
        full_track = os.path.join(album_wav_path, track)

        data, rate = sf.read(full_track)
        middle = round(len(data) / 2)
        half_width = int(1E4)
        meter = pyln.Meter(rate)
        core_data = data[middle - half_width:middle + half_width, :]
        loudness = meter.integrated_loudness(core_data)

        # clear the plot
        plt.clf()

        # Plot the signal read from wav dir
        plt.subplot(211)
        plt.title(track + ' [loudness: ' + str(loudness) + ']')
        plt.plot(core_data)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')

        plt.subplot(212)
        signal_data_avg = np.mean(core_data, axis=1)
        plt.specgram(signal_data_avg, Fs=rate, mode='psd', scale='dB')
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        # and save the plot
        plt.savefig(os.path.join(album_png_path, track + '.png'))


# process all tracks:
# - to wav files
# - generate visualizations
# - generate characteristicss
def __process_files(album_path, convert, plot, extract):
    album_mp3_path = os.path.join(album_path, 'mp3')
    album_wav_path = os.path.join(album_path, 'wav')
    album_png_path = os.path.join(album_path, 'png')
    album_csv_path = os.path.join(album_path, 'csv')

    os_tools.reset_dir(album_wav_path)
    os_tools.reset_dir(album_png_path)
    os_tools.reset_dir(album_wav_path)
    os_tools.reset_dir(album_csv_path)

    if convert:
        os_tools.log('converting files', 4)
        __convert_mp3_to_wav(album_mp3_path, album_wav_path)
    else:
        os_tools.log('skipping convert files', 4)

    if plot:
        os_tools.log('plotting files', 4)
        __music_visualizations(album_wav_path, album_png_path)
    else:
        os_tools.log('ignoring plot files', 4)


def process_all(convert, plot, extract):
    # get my dir
    data_dir = os.path.join(os.getcwd(), 'data')

    # walk the data directory and convert all mp3
    for album in os.listdir(data_dir):
        album_path = os.path.join(data_dir, album)

        # convert every album
        __process_files(album_path, convert, plot, extract)


process_all(False, False, True)

sys.exit(0)
