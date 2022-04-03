import csv
import os
import re
import sys
import warnings

import librosa
import librosa.display
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
sns.set(rc={'figure.figsize': (14, 12)})


def __convert_mp3_to_wav(album_mp3_path, album_wav_path):
    mp3_files = os.listdir(album_mp3_path)
    for mp3_file_name in mp3_files:

        os_tools.log(f'converting track {mp3_file_name}', 3)

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

    for track in audio_paths:
        # set the track name
        full_track = os.path.join(album_wav_path, track)

        os_tools.log(f'plotting track {track}', 3)

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

        # this is for plotting the whole track
        # spectrum properly, but is slow
        '''
        plt.subplot(313)
        x, sr = librosa.load(full_track)
        x_stf = librosa.stft(x)
        x_db = librosa.amplitude_to_db(abs(x_stf))
        librosa.display.specshow(x_db, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar()
        '''

        # and save the plot
        plt.savefig(os.path.join(album_png_path, track + '.png'))


def __generate_characteristics(album_wav_path, csv_file):
    audio_paths = os.listdir(album_wav_path)

    for track in audio_paths:

        full_track = os.path.join(album_wav_path, track)
        os_tools.log(f'analyzing track {track}', 3)

        track_name = re.sub('([ _#&,()-.\'])|(wav)', '', track, flags=re.IGNORECASE)
        os_tools.log(f'... named {track_name} |>', 3)
        y, sr = librosa.load(full_track, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{track_name} {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        file = open(csv_file, 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())


def __create_characteristics_csv_file():
    csv_file = os.path.join(os.getcwd(), 'gist_music.csv')
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header = header.split()
    try:
        os.remove(csv_file)
    except FileNotFoundError:
        os_tools.log('<~~ No feature file to delete ~~>', 4)
    finally:
        file = open(csv_file, 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    return csv_file


# process all tracks:
# - to wav files
# - generate visualizations
# - generate characteristics
def __process_files(album_path, convert, plot, extract, csv_file):
    album_mp3_path = os.path.join(album_path, 'mp3')
    album_wav_path = os.path.join(album_path, 'wav')
    album_png_path = os.path.join(album_path, 'png')

    if convert:
        os_tools.log('converting files', 4)
        os_tools.reset_dir(album_wav_path)
        __convert_mp3_to_wav(album_mp3_path, album_wav_path)
    else:
        os_tools.log('skipping convert files', 4)

    if plot:
        os_tools.log('plotting files', 4)
        os_tools.reset_dir(album_png_path)
        __music_visualizations(album_wav_path, album_png_path)
    else:
        os_tools.log('ignoring plot files', 4)

    if extract:
        os_tools.log('extracting characeristics from files', 4)
        __generate_characteristics(album_wav_path, csv_file)
    else:
        os_tools.log('ignoring characteristics of files', 4)


def process_all(convert, plot, extract):
    # get my dir
    data_dir = os.path.join(os.getcwd(), 'data')

    # create the csv file outside any loop
    csv_file = __create_characteristics_csv_file()

    # walk the data directory and convert all mp3
    for album in os.listdir(data_dir):
        album_path = os.path.join(data_dir, album)

        # convert every album
        __process_files(album_path, convert, plot, extract, csv_file)


process_all(True, True, True)

sys.exit(0)
