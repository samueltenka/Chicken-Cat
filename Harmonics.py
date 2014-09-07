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
   print(f, i)from Record_07 import Record, to_physical_time
from itertools import chain

R = Record(filename='data\\AAH220_brian.wav', duration=2.0)
S = R.sub(0.5, 0.5)

'''calculate intensities of frequencies'''
from math import pi, sin, cos, sqrt
def intensity(record, frequency):
   wave = Record(duration=record.duration, freq=frequency)
   return abs(wave.dot(record))

from itertools import chain
def harmonics(record):
   H = {}
   for f in range(2, 3000, 10):
      H[f] = intensity(record, f)
      for offset in range(2, 10, 2):
         H[f+offset] = H[f]
   return H

def reconstruct(H, dur):
   rtrn = Record(duration=dur)
   for f,coeff in H.items():
      print(f,end='')
      rtrn = rtrn.plus(Record(freq=f, duration=dur).times(coeff))
   return rtrn

S = S.times(1.0/(S.dot(S))**0.5)

H = harmonics(S)
print('harmonic strengths calculated!')
print('energy accounted for:', sum(i*i for f,i in H.items())**0.5)
S_ = reconstruct(H, dur=1.0)
print('reconstructed!')
S_.write_to('hi.wav')
print('written!')

##H = harmonics(S)
##print('strength scan completed!')
##for f, i in H.items():
##   print(f, i)
##print(sum(i*i for f,i in H.items())**0.5)

print(sum(i*i for f,i in H.items())**0.5)
