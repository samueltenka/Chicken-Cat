'''
Thx to
http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python
'''


import wave, struct

'''read wave into list of amplitudes in [-1, 1]'''
amplitudes = []
with wave.open('sam_ahh_0414.wav', 'r') as waveFile:
  length = waveFile.getnframes()
  for i in range(0,length):
      waveData = waveFile.readframes(1)
      data = struct.unpack("<h", waveData)
      amplitudes.append(data[0] / 32768.0)
print('done reading!')

#'''write binary'''
#with open('ahh.dat', 'wb') as dataFile:
#  for amp in amplitudes:
#    data = struct.pack('i', int(amp*32768))
#    dataFile.write(data)
#print('done writing!')

'''calculate intensities of frequencies'''
from math import pi, sin, cos, sqrt
def intensity_(frequency, t1, t2):
  amps_slice = amplitudes[int(t1*44100):int(t2*44100)]
  omega = 2*pi*frequency
  int_s = sum(amps_slice[i]*sin(omega*i/44100) for i in range(len(amps_slice)))
  int_c = sum(amps_slice[i]*cos(omega*i/44100) for i in range(len(amps_slice)))
  return sqrt(int_s**2 + int_c**2) * 2/len(amps_slice)
def intensity(frequency):
  return sum(intensity_(frequency, t, t+0.01) for t in [i/100 for i in range(100)]) / 100


for f in range(300, 450, 5):
  print(f, intensity(f))
