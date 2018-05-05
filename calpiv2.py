#!/usr/bin/env python3

from random import random
from time import perf_counter

DATRS = 1000*1000
hits  = 0.0
start =perf_counter()

for i in range(1,DATRS+1):
    x,y = random(),random()
    dist = pow(x ** 2 + y ** 2,0.5)
    if dist <= 1.0:
        hits = hits + 1
pi = 4 * (hits/DATRS)
print('pi:{}'.format(pi))
print('runtime:{:.5f}s'.format(perf_counter()-start))
