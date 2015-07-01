#-*- coding=utf-8 -*-

'''
Read in a WAV and find the freq's
'''

import pyaudio
import wave
import numpy as np
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_WAV_Freq(fileName):
    chunk = 4096*4
    # open up a wave
    wf = wave.open(fileName, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    CHANNELS = wf.getnchannels()
	
    # use a Blackman window
    window = np.blackman(chunk)
	
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = CHANNELS,
                    rate = RATE,
                    output = True)

    
	# read some data
    dataAll = wf.readframes(chunk)
    i=0
    i_L = 0
    i_R = 0
    freq_L = 0
    freq_R = 0
    
    # play stream and find the frequency of each chunk
    while len(dataAll) == chunk*swidth * 2:
        if i % 2 == 0:
            data = dataAll[0::2]
        else:
            data = dataAll[1::2]
        
		# write data out to the audio stream
        #stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))*window
        
		# Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        
		# find the maximum
        which = fftData[1:].argmax() + 1
        
		# use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
            
			# find the frequency and output it
            thefreq = (which+x1)*RATE/chunk        
        else:
            thefreq = which*RATE/chunk        
            
        if i % 2 == 0:
            if thefreq > 10 :
                i_L = i_L + 1
                freq_L += thefreq
                #print ("The left freq is : %f Hz." % (thefreq))
        else:
            if thefreq > 10 :
                i_R = i_R + 1
                freq_R += thefreq
                #print ("The right freq is : %f Hz." % (thefreq))
            
            
        # read more data
        dataAll = wf.readframes(chunk)
        i = i_L + i_R
        
    if dataAll:        
		#stream.write(data)
        pass

    avg_L = 0
    avg_R = 0
    try:
        avg_L = freq_L / i_L
        avg_R = freq_R / i_R
    except:
        pass
    finally:        
        stream.close()
        p.terminate()
    return "%.4f"%avg_L, "%.4f"%avg_R


if __name__ ==  '__main__':
    filename = SCRIPT_PATH + "\cap.wav"
    avg_L, avg_R = get_WAV_Freq(filename)
    print(avg_L, avg_R )
    
