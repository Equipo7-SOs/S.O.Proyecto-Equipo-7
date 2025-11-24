from .scheduler import Scheduler
from collections import deque

class FCFS(Scheduler):
    def __init__(self, processes=None):
        # Inicializamos vacío. Ignoramos 'processes' si llega.
        self.ready_queue = deque()
        self.current_process = None

    def add_to_queue(self, new_process):
        # Simplemente al final de la cola
        self.ready_queue.append(new_process)

    def choose_process(self):
        # 1. Si el proceso actual terminó, lo sacamos
        if self.current_process and self.current_process.is_finished():
            self.current_process = None

        # 2. Si no hay proceso corriendo, tomamos el siguiente de la fila
        if self.current_process is None:
            if self.ready_queue:
                self.current_process = self.ready_queue.popleft()
            else:
                return None

        return self.current_process

    def get_name(self):
        return "First Come, First Served"