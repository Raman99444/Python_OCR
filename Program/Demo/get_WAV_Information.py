 
'''
get the .wav file's information
'''

import pyaudio
import wave
import sys


wf = wave.open(r"c:\akm1ks_3.wav", 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

				
print(p)

