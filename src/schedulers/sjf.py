from .scheduler import Scheduler
#Este algoritmo implementa el Shortest Job First de la candelarización de procesos en el CPU
class SJF(Scheduler):

    def __init__(self, processes=None):
        self.ready_queue = [] # Cola de procesos
        self.current_process = None # Proceso actual

        if processes:
            # Ordenamos inicialmente por tiempo de llegada y burst time o tiempo en completar
            self.ready_queue = sorted(processes, key=lambda p: (p.arrival_time, p.burst_time))

    def add_to_queue(self, new_process):
        # Agregar nuevo proceso a la cola
        self.ready_queue.append(new_process)
        # Ordenar por burst time para elegir siempre al más corto
        self.ready_queue.sort(key=lambda p: p.burst_time)

    def choose_process(self):
        # Si tenemos un proceso ejecutándose y no ha terminado, entonces continuamos con él ya que no es preemtivo
        if self.current_process and self.current_process.remaining_time > 0:
            return self.current_process

        # Si ya no tenemos procesos, no hacer nada
        if not self.ready_queue:
            self.current_process = None
            return None

        # Tomamos el proceso en la posición 0, que siempre será el de menor burst time ya que los ordenamos antes
        self.current_process = self.ready_queue[0]

        # Si termina el proceso, lo quitamos
        if self.current_process.remaining_time == 0:
            self.ready_queue.pop(0)
            self.current_process = None
            return None
        # Si no ha terminado, lo regresamos como el proceso actual
        return self.current_process
