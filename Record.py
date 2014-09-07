import wave, struct
from math import sin, pi, sqrt

RATE = 44100
to_physical_time = lambda disc_ind: disc_ind/44100
to_discrete_ind = lambda phys_time: int(phys_time*44100)
duration_of = lambda amps: to_physical_time(len(amps))
make_range = lambda dur: range(to_discrete_ind(dur))

to_pressure = lambda pcm: pcm/32767
from_pressure = lambda press: int(max(-32767, min(+32767, press*32767)))

class Record:
   def __init__(self, filename='', source=None, duration=0.0, freq=0.0):
      if filename:
         self.read_from(filename, duration)
      elif source:
         if type(source) == type([]):
            self.copy_from(source)
         else:
            self.copy_from(source.amps)
      elif duration:
         if freq:
            self.generate_sin(duration, freq)
         else:
            self.generate_silence(duration)

   def copy_from(self, source):
      self.amps = source[:]
      self.duration = duration_of(self.amps)
   def read_from(self, filename, duration=0):
      ''' reads mono PCM16 '''
      ''' thx to http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python '''
      self.amps = []
      with wave.open(filename, 'r') as waveFile:
         length = waveFile.getnframes()
         if duration:
            length = min(length, to_discrete_ind(duration))
         for i in range(0,length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            self.amps.append(to_pressure(data[0]))
      self.duration = duration_of(self.amps)
   def generate_silence(self, dur):
      self.duration = dur
      self.amps = [0.0 for i in make_range(dur)]
   def generate_sin(self, dur, freq):
      self.duration = dur; omega = 2*pi*freq
      self.amps = [sin(omega*to_physical_time(i)) for i in make_range(dur)]

   def write_to(self, filename):
      with wave.open(filename, 'w') as waveFile:
        waveFile.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
        for a in self.amps:
          waveFile.writeframes(struct.pack('h', from_pressure(a)))
        
   def sub(self, start, dur):
      rtrn = Record(source=self.amps[to_discrete_ind(start):to_discrete_ind(start)+to_discrete_ind(dur)])
      if rtrn.duration != dur:
         print('!  ', start, dur)
         print('!  ', to_discrete_ind(start), to_discrete_ind(start+dur))
         print('!!!', rtrn.duration, dur)
      return rtrn
   def reverse(self):
      self.amps = self.amps[::-1]
   def join_from(self, subs):
      self.amps = []
      self.duration = 0.0
      for s in subs:
         self.amps += s.amps
      self.duration = duration_of(self.amps)

   def dot(self, other):
      if self.duration == other.duration:
         integral = sum(mine*theirs for mine,theirs in zip(self.amps, other.amps))
         return integral / self.duration
   def smart_dot(self, other):
      if self.duration == other.duration:
         segs = int(self.duration*50)
         starts = [i*0.02 for i in range(segs)]
         small_dots = [self.sub(t, 0.02).dot(other.sub(t, 0.02)) for t in starts]
         return sqrt(sum(sd*sd for sd in small_dots)) / segs
   def times(self, num):
      return Record(source=[a*num for a in self.amps])
   def plus(self, other):
      if self.duration == other.duration:
         return Record(source=[mine+theirs for mine,theirs in zip(self.amps, other.amps)])
   def minus(self, other):
      return self.plus(other.times(-1))
      

    
#R = Record(duration=1.0, freq=2*pi*440)
#print(R.dot(R)) ## get 22050 = 44100/2, correct

#S = Record(filename='C:\\Users\\Sam\\Desktop\\MHacks\\sam_ahh_0414.wav')
#R.write_to('hi.wav')
