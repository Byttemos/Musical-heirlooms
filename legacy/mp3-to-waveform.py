#!/usr/bin/env python3
from pytube import YouTube
import sys
from pydub import AudioSegment
#from pydub.utils import mediainfo
#import pydub
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
#from itertools import islice
# from matplotlib.colors import LinearSegmentedColormap as lsc

'''Audio preprocessing'''
#with open('source.mp4', 'rb') as file:
#    info = fleep.get(file.read(128))
#if info.extension == 'wav'

'''Audio file import'''
src = './ahmad.mp3'
audio = AudioSegment.from_file(src).split_to_mono()[0]
sample_rate = audio.frame_rate

'''Canvas setup'''
width, height = 200, 200
pixel_count = width*height

'''Construct numpy array and normalize data'''
samples = np.array(audio.get_array_of_samples())#[:int(0.5*sample_rate)]
samples = samples + np.abs(samples.min())
samples = samples - samples.mean()
samples = samples / np.max(samples)
bite = len(samples) // pixel_count

transformed_samples = fft(samples)
frequencies = fftfreq(transformed_samples.shape[-1], 1/int(sample_rate))

transformed_samples = transformed_samples[frequencies > 10]

frequencies = frequencies[frequencies > 10]

magnitude = np.abs(transformed_samples)
peak_index, properties = find_peaks(np.abs(transformed_samples), height = 1.5)

'''show fourier transformed array'''
# plt.plot(frequencies, np.abs(transformed_samples), '-', frequencies[peak_index], properties['peak_heights'], 'x')
# plt.show()

rgb_min = 0
rgb_max = 255
freq_min = 0
freq_max = max(magnitude) - np.mean(magnitude)
print(freq_max)
highest_freqs = frequencies[np.argpartition(transformed_samples, -3)[-3:]]

print('Highest frequencies in chunk: ' + str(highest_freqs))
def freqsToRGB(highest_freqs):
    '''Take three most prominent frequencies in a given chunk and map them to RGB-values (between 0 and 256)'''
    rgb_values = []
    for freq in highest_freqs:
        top_division = freq - rgb_min
        bot_division = freq_max - freq_min
        rgb_value = int((rgb_max-rgb_min)*(top_division/bot_division)+rgb_min)
        rgb_values.append(rgb_value)
    return rgb_values


# def chunks(lst, chunk_size):
#     bitable = iter(lst)
#     return iter(lambda: tuple(islice(bitable, chunk_size)), ())

canvas_array = []
en_chunk = len(samples) // pixel_count


for i in range(pixel_count):
    current_index = int(i * en_chunk)
    chunk = samples[current_index:current_index + en_chunk]
    transformed_chunk = fft(chunk)
    transformed_freq_chunk = fftfreq(transformed_chunk.shape[-1], 1/int(sample_rate))
    # transformed_freq_chunk = transformed_freq_chunk - np.mean(transformed_freq_chunk)
    top_freqs = np.abs(transformed_freq_chunk[np.argpartition(transformed_chunk, -3)[-3:]])
    canvas_array.append(freqsToRGB(top_freqs))
canvas = np.array(canvas_array)
print(canvas.shape)

canvas = canvas.reshape(width, height, 3)
# plt.plot(frequencies, magnitude)
# plt.show()
plt.imshow(canvas)
plt.show()
