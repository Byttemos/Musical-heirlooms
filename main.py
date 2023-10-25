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
for i in range(number_of_chunks):
    chunk = src[i * chunk_length : (i + 1) * chunk_length]
    avg_amplitude = np.sqrt(np.mean(np.array(chunk)**2))
    red_value = int(255 * (avg_amplitude / src.max_possible_amplitude))
    color = (red_value, 0, 0)
    color_array.append(color)

image = np.array(color_array, dtype = uint8).reshape(canvas['width'], number_of_chunks, 3)

plt.imshow(image)
plt.axis('off')
plt.show()