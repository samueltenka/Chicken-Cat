'''
Thx to
http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python
'''


import wave, struct

'''read wave into list of amplitudes in [-1, 1]'''
amplitudes = []
with wave.open('square_0440.wav', 'r') as waveFile:
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


def base_freq(min_f, max_f, S=5):
  '''finds strongest harmonic'''
  print(min_f, max_f)
  step = min(50, int((max_f-min_f)/S))
  if step!=0:
    diff = (max_f-min_f)/S
    freqs = [min_f + i*diff for i in range(S)]
    c = max((intensity(f), f) for f in freqs)[1]
    return base_freq(max(0, c-diff), c+diff)
  else:
    return max_f

print(base_freq(20, 20000))
