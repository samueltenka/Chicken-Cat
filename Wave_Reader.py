'''
Thx to
http://stackoverflow.com/questions/2060628/how-to-read-wav-file-in-python
'''


import wave, struct

waveFile = wave.open('square_0440.wav', 'r')
#waveFile = wave.open('sam_ahh_0372.wav', 'r')

length = waveFile.getnframes()
for i in range(0,length):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    print(int(data[0]))

