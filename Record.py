import wave, struct
from math import sin, pi

RATE = 44100
to_physical_time = lambda disc_ind: disc_ind/44100
to_discrete_ind = lambda phys_time: int(phys_time*44100)
duration_of = lambda amps: to_physical_time(len(amps))
make_range = lambda dur: range(to_discrete_ind(dur))

class Record:
   def __init__(self, filename='', source=None, duration=0.0, freq=0.0):
      if filename:
         self.read_from(filename)
      elif source:
         self.copy_from(source)
      elif duration:
         if freq:
            self.generate_sin(duration, freq)
         else:
            self.generate_silence(duration)

   def copy_from(self, other):
      self.duration = other.duration
      self.amps = other.amps[:]
   def read_from(self, filename):
      ''' reads mono PCM16 '''
      self.amps = []
      with wave.open(filename, 'r') as waveFile:
         length = waveFile.getnframes()
         for i in range(0,length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            self.amps.append(data[0] / 32768.0)
      self.duration = duration_of(self.amps)
   def generate_silence(self, dur):
      self.duration = dur
      self.amps = [0.0 for i in make_range(dur)]
   def generate_sin(self, dur, freq):
      self.duration = dur; omega = 2*pi*freq
      self.amps = [sin(omega*to_physical_time(i)) for i in make_range(dur)]
   def dot(self, other):
      if self.duration == other.duration:
         return sum(mine*theirs for mine,theirs in zip(self.amps, other.amps))

    
R = Record(duration=1.0, freq=2*pi*440)
print(R.dot(R)) ## get 22050 = 44100/2, correct

S = Record(filename='C:\\Users\\Sam\\Desktop\\MHacks\\sam_ahh_0414.wav')
