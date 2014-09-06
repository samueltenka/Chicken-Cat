from math import sin, pi

RATE = 44100
to_physical_time = lambda disc_ind: disc_ind/44100
to_discrete_ind = lambda phys_time: int(phys_time*44100)
duration_of = lambda amps: to_physical_time(len(amps))
make_range = lambda dur: range(to_discrete_ind(dur))

class Record:
  def __init__(self, source=None, duration=0.0, omega=0.0):
    if source:
      self.amps = source[:]
      self.duration = duration_of(self.amps)
    else:
      self.duration = duration
      if omega:
        self.amps = [sin(omega*to_physical_time(i)) for i in make_range(duration)]
      else:
        self.amps = [0.0 for i in make_range(duration)]
  
  def dot(self, other):
    if self.duration == other.duration:
      return sum(mine*theirs for mine,theirs in zip(self.amps, other.amps))

   
R = Record(source=None, duration=1.0, omega=2*pi*440)
print(R.dot(R)) ## get 22050 = 44100/2, correct
