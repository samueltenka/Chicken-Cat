from Record_04 import Record

'''read control and target samples, 2 seconds each:'''
sound_names = ['ahh',
               'ooh',
               'eeh',
               'aah',
               'euu',
               'huh',
               'lll',
               'mmm',
               'uhr',
               'ung']
training_pairs = {}
for name in sound_names:
   training_pairs[name] = (Record(duration=0.2, filename='data\\'+name.upper()+'220_brian.wav'),
                           Record(duration=0.2, filename='data\\'+name.upper()+'220_sam.wav'))
   print('read', name)

''' orthonormalize control samples (transforming target samples along for the ride '''
ons = {}
for name in sound_names:
   c, t = training_pairs[name]
   ## todo: normalize c,t to begin with, so brian doesn't speak louder than sam, etc.
   '''orthogonalize:'''
   oc, ot = c, t
   for prev in sound_names:
      if prev==name:
         break
      pc = ons[prev][0]
      coeff = c.dot(pc)
      oc = oc.minus(pc.times(coeff)); ot = ot.minus(pc.times(coeff))
   '''normalize:'''
   onc = oc.times(oc.dot(oc)**(-0.5)); ont = ot.times(oc.dot(oc)**(-0.5))
   ons[name] = (onc, ont)
   print('orthonormalized', name)
