from math import *

def f1(x):
    return x**2

def integrate(f, a, b, N=1000):
    dx = (b - a) / N
    total = 0
    for i in range(N):
        mid = a + (i + 0.5) * dx
        total += f(mid) * dx
    return total

def multi_int(f,lims):
    limits = []
    pass
        


print(integrate(f1,0,10))
l = [f1]
#print(l[0])
