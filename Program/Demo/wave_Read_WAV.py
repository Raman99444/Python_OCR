# -*- coding: utf-8 -*-

'''
read the .wav file's information.
'''

import wave
import numpy as np

def read_WAV(filename):
    # 打开WAV文档
    f = wave.open(filename, "rb")

    # 读取格式信息
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    #print(params)
    nchannels, sampwidth, framerate, nframes = params[:4]

    # 读取波形数据
    str_data = f.readframes(nframes)
    f.close()

    #将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    time = np.arange(0, nframes) * (1.0 / framerate)

    print(wave_data)
    print(time)


if __name__ == "__main__":
    read_WAV(r"c:\2.wav")
	
	