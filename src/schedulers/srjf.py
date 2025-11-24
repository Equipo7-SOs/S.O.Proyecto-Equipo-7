from .scheduler import Scheduler

class SRJF(Scheduler):
    def __init__(self, processes=None):
        self.ready_queue = []
        self.current_process = None
        

    def add_to_queue(self, new_process):
        self.ready_queue.append(new_process)

    def choose_process(self):
        # 1. Limpieza del proceso actual si ya terminó
        if self.current_process and self.current_process.remaining_time <= 0:
            if self.current_process in self.ready_queue:
                self.ready_queue.remove(self.current_process)
            self.current_process = None

        # 2. Si no hay procesos listos, CPU ociosa
        if not self.ready_queue:
            return None

        # 3. Elegir el proceso con menor tiempo restante
        best_candidate = min(
            self.ready_queue,
            key=lambda p: (p.remaining_time, p.arrival_time)
        )

        # 4. Apropiación
        if self.current_process is None:
            self.current_process = best_candidate
        elif best_candidate.remaining_time < self.current_process.remaining_time:
            self.current_process = best_candidate
        # Si empatan, mantenemos el actual

        return self.current_process

    def get_name(self):
        return "Shortest Remaining Job First (SRJF)"
