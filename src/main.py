import random
from process import Process
from simulation import Simulation
from schedulers.fcfs import FCFS
from schedulers.sjf import SJF
from schedulers.srjf import SRJF
from schedulers.rr import RoundRobin

def get_fresh_processes():
    # Devuelve lista base de procesos usados para validación cruzada
    return [
        Process(0, 0, 8),   # P0: Llega 0, Burst 8, "llega en tick 0, necesita 8 ticks de CPU"
        Process(1, 1, 4),   # P1: Llega 1, Burst 4
        Process(2, 2, 9),   # P2: Llega 2, Burst 9
        Process(3, 3, 5)    # P3: Llega 3, Burst 5
    ]


def generate_random_processes(n_procs=6, max_arrival=10, burst_min=1, burst_max=10, seed=None):
    """
    Genera n_procs procesos con arrival time aleatorio en [0, max_arrival]
    y burst en [burst_min, burst_max]. IDs se asignan de 0..n_procs-1.
    """

    # Si se proporciona semilla, fija el generador aleatorio
    if seed is not None:
        random.seed(seed)

    # Lista donde se almacenarán los procesos generados
    procs = []

    # Genera n_procs procesos
    for i in range(n_procs):
        # Tiempo de llegada aleatorio
        arrival = random.randint(0, max_arrival)
        # Burst aleatorio dentro del rango
        burst = random.randint(burst_min, burst_max)
        # Crea proceso y lo agrega a la lista
        procs.append(Process(i, arrival, burst))
    # Es importante que la simulation reciba la lista sin ordenar (la misma Simulation ordena usando arrival_time).
    return procs


def choose_user_processes():
    print("¿Deseas generar procesos aleatorios? (s/n) [s por defecto]")
    # Lee la decisión del usuario: s/n
    choice = input().strip().lower()
    # Cuando el usuario quiere procesos aleatorios
    if choice == 'n':
        try:
            # Se solicitan parámetros de generación
            n = int(input("Número de procesos (ej. 6): ").strip())
            max_arr = int(input("Máxima arrival time (ej. 10): ").strip())
            bmin = int(input("Burst mínimo (ej. 1): ").strip())
            bmax = int(input("Burst máximo (ej. 10): ").strip())
            seed_input = input("Semilla aleatoria (opcional, deja vacío para aleatorio): ").strip()
            # Convierte semilla si se dio una
            seed = int(seed_input) if seed_input != "" else None

            # Genera procesos con los parámetros dados
            procs = generate_random_processes(n, max_arr, bmin, bmax, seed=seed)
            print("\nProcesos generados:")
            # Muestra procesos ordenados por arrival_time para claridad
            for p in sorted(procs, key=lambda x: x.arrival_time):
                print(f"PID {p.pid} - arrival {p.arrival_time} - burst {p.burst_time}")
            
            # Regresa lista generada
            return procs

        except Exception as e:
            # En caso de error vuelve a procesos por defecto
            print("Entrada inválida, usando procesos por defecto. Error:", e)
            return get_fresh_processes()

    else:
        # Si dijo que no, usa procesos por defecto
        return get_fresh_processes()



def main():

    print("=== Simulador: FCFS, SJF, SRJF, Round Robin ===\n")

    # 1) elegir procesos (aleatorios o por defecto según elección del usuario)
    processes = choose_user_processes()

    # 2) elegir algoritmos a ejecutar (por simplicidad ejecutamos los 4)
    quantum = 2   # Quantum por defecto para Round Robin
    print(f"\nValor del quantum para Round Robin (valor por defecto = {quantum}). ¿Deseas cambiarlo? (s/n)")
    # Si el usuario quiere modificar el quantum
    if input().strip().lower() == 's':
        try:
            # Lee nuevo quantum
            quantum = int(input("Introduce quantum (ticks): ").strip())
        except:
            # Maneja error y conserva el valor actual
            print("Valor inválido, se mantiene quantum =", quantum)

    schedulers_to_test = [
        # Clase del algoritmo FCFS
        FCFS,
        # Clase del algoritmo SJF
        SJF,
        # Clase del algoritmo SRJF
        SRJF,
        # Round Robin requiere argumento → usamos lambda
        lambda: RoundRobin(quantum=quantum)  
    ]

    verbose = False
    print(f"\n¿Quieres que la simulación te indique qué hace en cada tick? (s/n)")
    if input().strip().lower() == 's':
        try:
            verbose = True
        except: 
            # Si no tenemos un input válido asumimos que no 
            print("Valor inválido, la simulación no dirá qué hace en cada tick")

    print("=== INICIANDO VALIDACIÓN CRUZADA ===")

    # Itera sobre cada algoritmo
    for SchedulerClass in schedulers_to_test:
        # 1. Instanciar datos limpios de los procesos
        procs = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in processes]
        # 2. Instanciar el scheduler
        scheduler = SchedulerClass()
        # 3. Instanciar simulación, crea una simulación con el scheduler dado y procesos
        sim = Simulation(scheduler, procs, verbose)
        
        # 4. Correr la simulación
        sim.simulate()
        print("\n" + "="*40 + "\n")

# Punto de entrada del programa
if __name__ == "__main__":
    main()