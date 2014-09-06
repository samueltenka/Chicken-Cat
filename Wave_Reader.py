'''
Thx to
http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python
'''


import wave, struct

amplitudes = []
with wave.open('sam_ahh_0372.wav', 'r') as waveFile:
  length = waveFile.getnframes()
  for i in range(0,length):
      waveData = waveFile.readframes(1)
      data = struct.unpack("<h", waveData)
      amplitudes.append(data[0] / 32768.0)
print('done reading!')


from math import pi, sin, cos, sqrt
def intensity(frequency, t1, t2):
  amps_slice = amplitudes[int(t1*44100):int(t2*44100)]
  omega = 2*pi*frequency
  int_s = sum(amps_slice[i]*sin(omega*i/44100) for i in range(len(amps_slice)))
  int_c = sum(amps_slice[i]*cos(omega*i/44100) for i in range(len(amps_slice)))
  return sqrt(int_s**2 + int_c**2) * 2/len(amps_slice)
