from metrics import Metrics

class Simulation:
    def __init__(self, scheduler, processes=[], verbose=True):
        # Reloj global de la simulación, inicia en 0
        self.current_tick = 0 
        # Scheduler seleccionado (FCFS, SJF, SRJF o RR)
        self.scheduler = scheduler 
        
        # 1. Guardamos los procesos "futuros" ordenados por llegada
        # Usamos list(...) para crear una copia y no afectar la lista original
        self.incoming_processes = sorted(list(processes), key=lambda p: p.arrival_time)
        
        # Indica si queremos que la simulacion imprima lo que esta haciendo en cada tick
        self.verbose = verbose

        # Creamos un objeto Metrics asociado a este algoritmo
        self.reporter = Metrics(self.scheduler.get_name())
        # Registramos todos los procesos en el reportero desde el inicio (aunque aún no lleguen)
        for p in processes:
            # Registrar cada proceso para métricas finales
            self.reporter.add_to_processes(p)

     # Avanza el reloj global en +1
    def increment_tick(self):
        self.current_tick += 1

    def tick(self):
        # 2. FASE DE LLEGADA: Mover procesos de "incoming" a "ready" (Scheduler)
        # Mientras haya procesos y el primero de la lista llegue AHORA:
        while self.incoming_processes and self.incoming_processes[0].arrival_time == self.current_tick:
            # Extrae el proceso que "llega"
            process_arriving = self.incoming_processes.pop(0)
            # Lo pasa a la cola de listos del scheduler
            self.scheduler.add_to_queue(process_arriving)
            
            print(f"[Tick {self.current_tick}] Process ID {process_arriving.pid} arrived.")

        # 3. FASE DE EJECUCIÓN: El Scheduler elige quién corre
        current_process = self.scheduler.choose_process()   # Puede devolver un proceso o None (CPU Idle) 

        if current_process:
            # Ejecutamos 1 tick del proceso (reduce remaining_time en 1)
            current_process.set_remaining_time(1, self.current_tick) 
            if self.verbose:
                print(f"Process ID {current_process.pid} running at tick {self.current_tick}")
            
            # NECESARIO PARA ROUND ROBIN
            #  Verifica si el scheduler tiene el método especial on_tick_executed()
            if hasattr(self.scheduler, "on_tick_executed"):
                # Llama a la función que reduce el "quantum" restante tick a tick (para RR).
                self.scheduler.on_tick_executed()

            # Actualizamos métricas (CPU ocupado en ese tick)
            self.reporter.increase_counter_time(used_cpu=True)
            # Registramos cuál proceso se ejecutó en este tick (para el Gantt)
            self.reporter.log_execution(current_process.pid)
        else:
            # CPU Ocioso (Idle)
            if self.verbose:
                print(f"[Tick {self.current_tick}] CPU Idle")
            # CPU estuvo inactiva este tick
            self.reporter.increase_counter_time(used_cpu=False)
            # Registrar tick Idle (se representa como None)
            self.reporter.log_execution(None)

        # 4. Calcular métricas y avanzar reloj
        self.reporter.compute_metrics()
        # Avanzar el reloj después de terminar el tick
        self.increment_tick()

        # Retornamos True si todavía hay trabajo pendiente (procesos llegando o en cola)
        return True 

    def simulate(self):
        print(f"--- Starting Simulation: {self.scheduler.get_name()} ---")
        
        # La simulación corre mientras:
        # 1. Queden procesos por llegar (incoming_processes no vacío)
        # 2. O, queden procesos activos (chequeamos con metrics si finished < total)
        
        simulation_active = True
        while simulation_active:
            # Ejecuta un ciclo completo
            self.tick()
            
            #  Contar cuántos procesos están terminados
            finished_count = len([p for p in self.reporter.processes.values() if p.is_finished()])
            total_count = len(self.reporter.processes)
            
            # Condición de parada: 
            # Si no hay procesos entrando Y todos los procesos registrados han terminado
            if not self.incoming_processes and finished_count == total_count:
                # Cortamos el ciclo
                simulation_active = False

        # Imprime métricas finales y Gantt
        self.reporter.print_compact_gantt()
        print(self.reporter)