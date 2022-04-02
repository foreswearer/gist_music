# import the pyplot and wavfile modules

import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pyloudnorm as pyln
import seaborn as sns
import soundfile as sf
from numpy.core._exceptions import UFuncTypeError
from scipy.io import wavfile

sns.set()
sns.set(rc={'figure.figsize': (11.7, 8.27)})

current_path = os.getcwd()
data_path = os.path.join(current_path, 'data')
dirfiles = os.listdir(data_path)
fullpaths = map(lambda name: os.path.join(data_path, name), dirfiles)

root_dirs = []

for root_dir in fullpaths:
    if os.path.isdir(root_dir): root_dirs.append(root_dir)


def music_visualizations(album):
    wav_dir = os.path.join(album, 'wav')
    image_dir = os.path.join(album, 'png')
    audio_paths = os.listdir(wav_dir)
    try:
        shutil.rmtree(image_dir)
    except OSError:
        pass
    try:
        os.mkdir(image_dir)
    except OSError:
        pass

    for song in audio_paths:

        song_full = os.path.join(wav_dir, song)
        # Read the wav dir (mono)
        sampling_frequency, signal_data = wavfile.read(song_full)

        middle = round(len(signal_data) / 2)
        half_width = int(1E4)
        signal_data = signal_data[middle - half_width:middle + half_width, :]

        data, rate = sf.read(song_full)
        meter = pyln.Meter(rate)  #
        data = data[middle - half_width:middle + half_width, :]
        loudness = meter.integrated_loudness(data)

        # clear the plot
        plt.clf()

        # Plot the signal read from wav dir
        plt.subplot(211)
        plt.title(song + ' [loudness: ' + str(loudness) + ']')
        plt.plot(data)  # we can use data or signal_data. TODO: investigate which one is better
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')

        # TODO: improve visualization
        plt.subplot(212)
        signal_data_avg = np.mean(data, axis=1)

        # also, possible get one channel
        # plt.specgram(signal_data[:,0], Fs=sampling_frequency)
        plt.specgram(signal_data_avg, Fs=sampling_frequency, mode='psd', scale='dB')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        try:
            plt.savefig(os.path.join(image_dir, song + '.png'))
        except UFuncTypeError as ufte:
            print(ufte + ' ' + song)


for root_dir in root_dirs:
    music_visualizations(root_dir)
