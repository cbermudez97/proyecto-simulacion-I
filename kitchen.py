from queue import Queue

class Kitchen:
    def __init__(self, agen, sushitimegen, sandwichtimegen, typegen, duration, working):
        self.agen = agen # Generador de tiempo entre arribos
        self.sushitimegen = sushitimegen # Generador de tiempo de preparacion de sushi
        self.sandwichtimegen = sandwichtimegen # Generador de tiempo de preparacion de sandiwch
        self.typegen = typegen # Generador de tipo de pedido True -> sushi False -> sandwich
        self.working = working # Para un momento de tiempo dado cuantos trabajadores hay disponibles(Para implementacion mas general)

        self.ta = agen() # Tiempo del siguiente evento de arribo
        self.th1 = duration + self.ta # Tiempo del siguiente evento de salida de un cliente atendido por el empleado 1
        self.th2 = duration + self.ta # Tiempo del siguiente evento de salida de un cliente atendido por el empleado 2
        self.oth1 = False # El empleado 1 esta ocupado
        self.oth2 = False # El empleado 2 esta ocupado
        self.t = 0 # Tiempo actual
        self.T = duration # Tiempo del final de la simulacion
        
        self.queue = Queue() # Cola de arribos al puesto
        
        self.Na = 0 # Cantidad de personas que estan en  el sistema
        self.Nd = 0 # Cantidad de personas que salieron del sistema
        self.th1_a = 0 # Tiempo de arribo del cliente que se esta atendiendo con el empleado 1
        self.th2_a = 0 # Tiempo de arribo del cliente que se esta atendiendo con el empleado 2

        self.late_n = 0 # Cantidad de personas que se demoraron mas de 5 minutos hasta ser atendidas

    def gen_order_time(self): # Genera tiempo de duracion en completar una orden
        # Se asume que se pide un solo plato
        # Para pedir mas de uno se puede sobreescribir este metodo
        return self.sushitimegen() if self.typegen() else self.sandwichtimegen()

    def advance(self):
        event = min(self.ta, self.th1, self.th2)
        self.time = event
        if event == self.ta and event <= self.T: # Ocurre un arribo
            self.Na += 1
            self.ta = self.time + self.agen()
            if not self.oth1: # Intenta ser atendido por el empleado 1
                self.th1_a = event
                self.th1 = self.time + self.gen_order_time()
                self.oth1 = True
            elif not self.oth2: # Intenta ser atendido por el empleado 2
                self.th2_a = event
                self.th2 = self.time + self.gen_order_time()
                self.oth1 = True
            else: # Pasa a la cola
                self.queue.put_nowait(event)
            return True
        elif event == self.th1: # Termina un cliente atendido por el empleado 1
            self.Na -= 1
            self.Nd += 1
            elapsed = event - self.th1_a
            self.late_n += (1 if elapsed > 5 else 0)
            if not self.queue.empty(): # Existen personas en la cola
                self.th1_a = self.queue.get_nowait()
                self.th1 = self.time + self.gen_order_time()
            else: # La cola esta vacia
                self.th1 = self.time + self.ta
                self.oth1 = False
            return True
        elif event == self.th2: # Termina un cliente atendido por el empleado 2
            self.Na -= 1
            self.Nd += 1
            elapsed = event - self.th2_a
            self.late_n += (1 if elapsed > 5 else 0)
            if not self.queue.empty(): # Existen personas en la cola
                self.th2_a = self.queue.get_nowait()
                self.th2 = self.time + self.gen_order_time()
            else: # La cola esta vacia
                self.th2 = self.time + self.ta
                self.oth2 = False
            return True
        assert self.Na == 0, "No pueden quedar personas al final de la simulacion"
        return False
