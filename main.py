import fleep
from pydub import AudioSegment
from os import path
import numpy as np
import matplotlib.pyplot as plt

'''Audio preprocessing'''

preproc_src = '/home/hriskaer/kode/musical_heirlooms/ahmad.mp3'
print('Checking file type...')
with open(preproc_src, 'rb') as file:
    info = fleep.get(file.read(128))
if info.extension == ['wav']:
    print('file is a wav file, Continuing')
    
elif info.extension == ['mp3']:
    print('file is an mp3 file. Converting...')
    preproc_src = AudioSegment.from_mp3(preproc_src)
    preproc_src.export('/home/hriskaer/kode/musical_heirlooms/source.wav', format='wav')

elif info.extension == ['mp4']:
    print('file is an mp4 file. Converting...')
    preproc_src = AudioSegment.from_file(preproc_src)
    preproc_src.export('/home/hriskaer/kode/musical_heirlooms/source.wav', format='wav')
else:
    print('Format unaccounted for. format is ' + str(info.extension))
    print('Quitting')
    exit()


'''Import waveform and post processing'''
src = '/home/hriskaer/kode/musical_heirlooms/source.wav'
audio = AudioSegment.from_file(src).split_to_mono()[0]
sample_rate = audio.frame_rate
print('Waveform imported. Sample rate: ' + str(sample_rate))


'''Establish canvas'''
canvas = {'width':10, 'height':10}
number_of_chunks = canvas['height']
chunk_length = len(src) // number_of_chunks
color_array = []
print('Canvas dimensions: ' + str(canvas))
print('Chunk length: ' + str(chunk_length))


'''Populate color array'''
