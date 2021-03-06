''' thx to http://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
for explaining FFT '''


from math import pi, cos, sin

expi = lambda theta: cos(theta)+1j*sin(theta)

def dot(l1, l2):
   if len(l1)==len(l2):
      return sum(x1*x2 for x1,x2 in zip(l1, l2))
def plus(l1, l2):
   if len(l1)==len(l2):
      return [x1+x2 for x1,x2 in zip(l1, l2)]
def times(l1, l2):
   if len(l1)==len(l2):
      return [x1*x2 for x1,x2 in zip(l1, l2)]
def wave(length, dtheta):
   return [expi(n*dtheta) for n in range(length)]

def SFT(my_list):
   coeffs = []
   N = len(my_list)
   for i in range(N):
      w = wave(len(my_list), -2*pi*i/N)
      coeffs.append(dot(my_list,w))
   return coeffs

def FFT(my_list):
   ''' assumes my_list has power-of-two length. '''
   N = len(my_list)
   if N <= 32:
      return SFT(my_list)
   else:
      evens, odds = FFT(my_list[::2]), FFT(my_list[1::2])
      phase_shifts = wave(N, -2*pi/N)
      return plus(evens+evens, times(odds+odds, phase_shifts))

def IFFT(coefficients):
   conjugated = [c.conjugate() for c in coefficients]
   return [c/len(coefficients) for c in FFT(conjugated)]

from random import random
S1_rand = lambda: expi(random()*2*pi)
a = [S1_rand() for i in range(256)]
f = FFT(a)
b = IFFT(f)
print('|b-a|^2:', sum((abs(bb-aa))**2 for aa,bb in zip(a, b)))
print('sum of energies:', sum((abs(ff)/len(a))**2 for ff in f))
