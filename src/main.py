from process import Process
from simulation import Simulation
from schedulers.fcfs import FCFS
from schedulers.sjf import SJF
from schedulers.srjf import SRJF

def get_fresh_processes():
    return [
        Process(0, 0, 8),   # P0: Llega 0, Burst 8
        Process(1, 1, 4),   # P1: Llega 1, Burst 4
        Process(2, 2, 9),   # P2: Llega 2, Burst 9
        Process(3, 3, 5)    # P3: Llega 3, Burst 5
    ]

# Lista de algoritmos a probar
schedulers_to_test = [FCFS, SJF, SRJF]

print("=== INICIANDO VALIDACIÓN CRUZADA ===")

for SchedulerClass in schedulers_to_test:
    # 1. Instanciar datos limpios
    procs = get_fresh_processes()
    # 2. Instanciar algoritmo
    scheduler = SchedulerClass()
    # 3. Instanciar simulación
    sim = Simulation(scheduler, procs)
    
    # 4. Correr
    sim.simulate()
    print("\n" + "="*40 + "\n")