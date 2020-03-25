from sys import argv
from kitchen import Kitchen
from distributions import exponential, rand, Ber, mean

assert len(argv) >= 2, "Se debe especificar el lambda a utilizar para las llegadas de clientes"

l = float(argv[1])

def agen():
    return exponential(l)

def sushitimegen():
    return rand(5,8)

def sandwichtimegen():
    return rand(3, 5)

def typegen():
    return Ber(1/2)

def working(t):
    return 2

def working_with_help(t):
    if 90 <= t and t <= 210:
        return 3
    if 420 <= t and t <= 540:
        return 3
    return 2

print(f'Corriendo simulacion usando lambda={l}')
times = 1000
results = []
print(f'Realizando {times} simulacion(es) sin ayudante:')
for _ in range(times):
    model = Kitchen(agen, sushitimegen, sandwichtimegen, typegen, 660, 2, working)
    while model.advance():
        # input('Presione entar para continuar...')
        pass
    results.append((model.late_n*100)/model.Nd)
prom = mean(results)
print(f'2 Empleados {prom}%')

times = 1000
results = []
print(f'Realizando {times} simulacion(es) con ayudante:')
for _ in range(times):
    model = Kitchen(agen, sushitimegen, sandwichtimegen, typegen, 660, 3, working_with_help)
    while model.advance():
        # input('Presione entar para continuar...')
        pass
    results.append((model.late_n*100)/model.Nd)
prom = mean(results)
print(f'2 Empleados con ayudante {prom}%')
