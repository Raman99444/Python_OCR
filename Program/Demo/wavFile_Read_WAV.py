from scipy.io import wavfile # get the api
from scipy import fft, arange

fs, data = wavfile.read(r'c:\akm1ks_10.wav') # load the data
a = data.T[1] # this is a two channel soundtrack, I get the first track
#print(a)
b= [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
#print(b)
c = fft(b) # create a list of complex number
#print(c)
d = len(c)/2  # you only need half of the fft list
#print(d)
k = arange(len(data))
T = len(data)/fs
frqLabel = k/T
print(frqLabel)
