from Record_05 import Record
from Orthogonalizer_05 import sound_names, ons

''' read & segment: '''
#v = Record(filename='inputted_brian_voice.wav')
v = Record(filename='data\\HUH220_brian.wav')
segs = int(v.duration/0.1)-1
starts = [i*0.1 for i in range(segs)]
vsubs = [v.sub(t, 0.1) for t in starts]
print('read input')

''' translate '''
wsubs = []
for vs in vsubs:
   ws = Record(duration=0.1)
   error = Record(source=vs)
   for name in sound_names:
      c, t = ons[name]
      if vs.duration != c.duration:
         print(vs.duration, c.duration)
         continue
      coeff = vs.smart_dot(c)
      ws = ws.plus(t.times(coeff))
      error = error.minus(c.times(coeff))
   ws = ws.plus(error)
   wsubs.append(ws)
print('translated! :)))')

''' join & write: '''
w = Record()
w.join_from(wsubs)
w.write_to('generated_sam_voice.wav')
print('wrote!')
