from Record_07 import Record, to_physical_time

R = Record(filename='data\\AAH220_brian.wav', duration=2.0)
S = R.sub(1.0, 0.02)

'''calculate intensities of frequencies'''
from math import pi, sin, cos, sqrt
def intensity(record, frequency):
   wave = Record(duration=record.duration, freq=frequency)
   return abs(wave.dot(record))

from itertools import chain
def harmonics(record):
   #freqs = [n*base_freq for n in range(1, 65)]
   freqs = range(25, 2000, 25)
   return {f:intensity(record, f) for f in freqs}

S = S.times(1.0/(S.dot(S))**0.5)
H = harmonics(S)
print('strength scan completed!')
for f, i in H.items():
   print(f, i)
print(sum(i*i for f,i in H.items())**0.5)
