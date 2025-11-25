from .scheduler import Scheduler
from collections import deque

# Definimos Clase RoundRobin, que hereda de Scheduler
class RoundRobin(Scheduler):
    def __init__(self, quantum=2, processes=None):
        """
        quantum: tamaño de time slice en ticks (int)
        processes: no usado aquí; la simulación se encarga de inyectar procesos
        """
        # Cola de listos (FIFO)
        self.ready_queue = deque()
        # Referencia al proceso ejecutándose actualmente 
        self.current_process = None
        # quantum total que se le da a un proceso cuando comienza a ejecutarse
        self.quantum = quantum
        # contador de quantum restante para el proceso actual
        self.quantum_remaining = 0

    def add_to_queue(self, new_process):
        # Añadir al final de la cola de listos
        self.ready_queue.append(new_process)

    def choose_process(self):
        """
        Lógica por tick:
        - Si current terminó, lo limpiamos.
        - Si current existe y aún tiene quantum_remaining > 0 y no terminó -> sigue corriendo.
        - Si current existe pero quantum_remaining == 0 -> se pone al final (si no terminó) y sacamos el siguiente.
        - Si no hay current, sacamos el siguiente de la cola.
        """
        # 1) Si el proceso actual terminó, lo limpiamos
        if self.current_process and self.current_process.is_finished():
            # Libera el proceso actual
            self.current_process = None
            # Reinicia contador de quantum
            self.quantum_remaining = 0

        # 2) Si hay proceso corriendo y tiene quantum restante, lo dejamos seguir
        if self.current_process and self.quantum_remaining > 0:
            return self.current_process

        # 3) Si había proceso pero se acabó su quantum y aún no terminó -> lo re-enqueue
        if self.current_process and not self.current_process.is_finished():
            # Re-enqueue al final
            self.ready_queue.append(self.current_process)
            # Se libera CPU
            self.current_process = None
            # Reinicia contador
            self.quantum_remaining = 0

        # 4) Si hay procesos en cola, tomar el siguiente
        if self.ready_queue:
            # Se toma el primero en la cola
            self.current_process = self.ready_queue.popleft()
            # asignamos quantum completo al comenzar o reanudarse
            self.quantum_remaining = self.quantum
            # Este ejecutará ahora
            return self.current_process

        # 5) Si no hay nadie listo -> CPU idle
        return None

    def on_tick_executed(self):
        """
        Este método es llamado por Simulation después de que un tick fue ejecutado.
        Tiene el propósito de reducir el quantum_remaining del proceso actual.
        """
        if self.current_process and self.quantum_remaining > 0:
            # Decrementa el quantum usado en este tick
            self.quantum_remaining -= 1

    def get_name(self):
        return f"Round Robin (quantum={self.quantum})"
