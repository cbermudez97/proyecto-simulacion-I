from queue import Queue

class Kitchen:
    def __init__(self, agen, sushitimegen, sandwichtimegen, typegen, duration, maxn, working):
        self.agen = agen # Generador de tiempo entre arribos
        self.sushitimegen = sushitimegen # Generador de tiempo de preparacion de sushi
        self.sandwichtimegen = sandwichtimegen # Generador de tiempo de preparacion de sandiwch
        self.typegen = typegen # Generador de tipo de pedido True -> sushi False -> sandwich
        self.working = working # Para un momento de tiempo dado cuantos empleados hay disponibles(Para implementacion mas general)
        self.maxn = maxn # Cantidad maxima de empleados

        self.ta = agen() # Tiempo del siguiente evento de arribo
        self.th = [duration + self.ta] * self.maxn # Tiempo del siguiente evento de salida de un cliente atendido por el empleado i
        self.oth = [False] * self.maxn # El empleado i esta ocupado
        self.t = 0 # Tiempo actual
        self.T = duration # Tiempo del final de la simulacion
        
        self.queue = Queue() # Cola de arribos al puesto
        
        self.Na = 0 # Cantidad de personas que estan en  el sistema
        self.Nd = 0 # Cantidad de personas que salieron del sistema

        self.late_n = 0 # Cantidad de personas que se demoraron mas de 5 minutos hasta ser atendidas

    def gen_order_time(self): # Genera tiempo de duracion en completar una orden
        # Se asume que se pide un solo plato
        # Para pedir mas de uno se puede sobreescribir este metodo
        return self.sushitimegen() if self.typegen() else self.sandwichtimegen()

    def advance(self):
        event = min(self.ta, *self.th)
        self.time = event
        current_workers = self.working(self.time)
        assert current_workers <= self.maxn, "No pueden trabajar mas empleados que la cantidad maxima"
        if event == self.ta: # Ocurre un arribo
            if event <= self.T:
                self.Na += 1
                self.ta = self.time + self.agen()
                for i in range(current_workers): # Solo se tienen en cuenta los empleados que estan trabajando en ese momento
                    if not self.oth[i]: # Intenta ser atendido por el empleado i
                        self.th[i] = self.time + self.gen_order_time()
                        self.oth[i] = True
                        return True
                # Pasa a la cola
                self.queue.put_nowait(event)
                return True
            else:
                self.ta = max(*self.th) + 1
                return any(self.oth)
        for i in range(self.maxn):
            if event == self.th[i]: # Termina un cliente atendido por el empleado 1
                self.Na -= 1
                self.Nd += 1    
                if not self.queue.empty() and i < current_workers: # Existen personas en la cola y el empleado sigue trabajando
                    arrival = self.queue.get_nowait()
                    elapsed = event - arrival
                    self.late_n += (1 if elapsed > 5 else 0)
                    self.th[i] = self.time + self.gen_order_time()
                else: # La cola esta vacia
                    self.th[i] = self.T + self.ta
                    self.oth[i] = False
                return True
        assert self.Na == 0, "No pueden quedar personas al final de la simulacion"
        return False
