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
	
    save_wave_file(filename, save_buffer)
    save_buffer = []
    print (filename + " saved")

	
'''
save the date to the wav file
'''
def save_wave_file(filename, data):
    #define of params
	#The setting need same with the 'record_wave' function define.
    framerate = 44100 
    channels = 2
    width = 2
    
    #save the date to the wav file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(width)
    wf.setframerate(framerate)
    wf.writeframes("".join(data))
    wf.close()

if __name__ == "__main__":
    filename = SCRIPT_PATH + "\cap.wav"
    record_wave(filename)

