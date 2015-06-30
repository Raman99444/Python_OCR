# -*- coding: utf-8 -*-

'''
capture the sound sigle and save it 
'''

import numpy as np
from pyaudio import PyAudio, paInt16
from datetime import datetime
import wave
import os


'''
capture the wave single
'''
def record_wave(filename):
    #define of params
    NUM_SAMPLES = 20000
    framerate = 44100
    
    #record time
    TIME = 4
    
    #open the input of wave
    pa = PyAudio()
    stream = pa.open(format = paInt16, channels = 2,
          rate = framerate, input = True,
          frames_per_buffer = NUM_SAMPLES)
    save_buffer = []
    count = 0
    while count < TIME:
        #read NUM_SAMPLES sampling data
        string_audio_data = stream.read(NUM_SAMPLES)
        save_buffer.append(string_audio_data)
        count += 1
        print ('recoding......')
	
	

record_wave(r'c:\cap.wav')

