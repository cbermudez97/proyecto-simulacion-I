from random import random
from scipy import floor, log, e

def rand(a, b):
    return (b-a)*random() + a

def rand_int(a,b):
    return floor((b-a)*random()) + a

def Ber(p):
    return 1 if random() < p else 0

def Bin(n, p):
    return sum(( Ber(p)  for _ in range(n) ))

def poisson(l):
    u = random()
    n = 0
    fact = 1
    s = 0
    while True:
        s += (l**n)*e**(-l)/fact
        if s > u:
            break
        n += 1
        fact *= n
    return n

def exponential(l):
    return -log(random())/l

def PoiProcess(l, t):
    time = 0
    cant = 0
    events = []
    while True:
        time += exponential(l)
        if time > t:
            break
        events.append(time)
        cant += 1
    return events

def Gamma(n,l):
    return sum([exponential(l) for _ in range(n)])

def mean(l):
    return sum(l)/len(l)

def variance(l):
    var = 0
    m = mean(l)
    for xi in l:
        var += (xi - m)**2/(len(l)-1)
    return var
