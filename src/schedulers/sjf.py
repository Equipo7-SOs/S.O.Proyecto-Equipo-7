from .scheduler import Scheduler

class SJF(Scheduler):
    def __init__(self, processes=None):
        self.ready_queue = []
        self.current_process = None

    def add_to_queue(self, new_process):
        self.ready_queue.append(new_process)

    def choose_process(self):
        # --- LÓGICA NO APROPIATIVA ---
        # Si hay un proceso corriendo y NO ha terminado, SIGUE corriendo.
        # No importa si llegó alguien más corto.
        if self.current_process and not self.current_process.is_finished():
            return self.current_process

        # --- SELECCIÓN DE NUEVO PROCESO ---
        # Si llegamos aquí, es porque el CPU está libre (current es None o terminó)
        
        # 1. Limpiamos referencias viejas si existen
        if self.current_process and self.current_process.is_finished():
             self.current_process = None

        # 2. Si no hay nadie en espera, retornamos None
        if not self.ready_queue:
            return None

        # 3. Elegimos el proceso con menor BURST TIME original
        # Nota: En SJF clásico se usa el burst total, no el remaining.
        # Desempate por llegada.
        best_candidate = min(
            self.ready_queue, 
            key=lambda p: (p.burst_time, p.arrival_time)
        )
        
        # Lo sacamos de la cola de listos y lo ponemos en CPU
        self.ready_queue.remove(best_candidate)
        self.current_process = best_candidate
        
        return self.current_process

    def get_name(self):
        return "Shortest Job First (Non-Preemptive)"