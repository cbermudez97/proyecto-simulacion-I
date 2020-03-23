from kitchen import Kitchen
from distributions import exponential, rand, Ber, mean


def agen():
    return exponential(0.25)

def sushitimegen():
    return rand(5,8)

def sandwichtimegen():
    return rand(3, 5)

def typegen():
    return Ber(1/2)

def working(t):
    return 2


times = 1000
results = []
print(f'Realizando {times} simulacion(es):')
for _ in range(times):
    model = Kitchen(agen, sushitimegen, sandwichtimegen, typegen, 660, 2, working)
    while model.advance():
        # input('Presione entar para continuar...')
        pass
    results.append((model.late_n*100)/model.Nd)
prom = mean(results)
print(f'El porciento de personas que demoraron mas de 5 minutos en ser atendidas es del {prom}%')
