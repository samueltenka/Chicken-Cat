from Record import Record

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
   training_pairs[name] = (Record(duration=2.0, filename='data\\'+name.upper()+'220_brian.wav'),
                           Record(duration=2.0, filename='data\\'+name.upper()+'220_sam.wav'))
   print('read', name)
