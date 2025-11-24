from metrics import Metrics

class Simulation:
    def __init__(self, scheduler, processes=[]):
        self.current_tick = 0 
        self.scheduler = scheduler 
        
        # 1. Guardamos los procesos "futuros" ordenados por llegada
        # Usamos list(...) para crear una copia y no afectar la lista original
        self.incoming_processes = sorted(list(processes), key=lambda p: p.arrival_time)
        
        self.reporter = Metrics(self.scheduler.get_name())
        # Registramos todos los procesos en el reportero desde el inicio
        for p in processes:
            self.reporter.add_to_processes(p)

    def increment_tick(self):
        self.current_tick += 1

    def tick(self):
        # 2. FASE DE LLEGADA: Mover procesos de "incoming" a "ready" (Scheduler)
        # Mientras haya procesos y el primero de la lista llegue AHORA:
        while self.incoming_processes and self.incoming_processes[0].arrival_time == self.current_tick:
            process_arriving = self.incoming_processes.pop(0)
            self.scheduler.add_to_queue(process_arriving)
            print(f"[Tick {self.current_tick}] Process ID {process_arriving.pid} arrived.")

        # 3. FASE DE EJECUCIÓN: El Scheduler elige quién corre
        current_process = self.scheduler.choose_process() 

        if current_process:
            # Ejecutamos el proceso
            current_process.set_remaining_time(1, self.current_tick) 
            print(f"Process ID {current_process.pid} running at tick {self.current_tick}")
            
            # Actualizamos métricas (CPU ocupado)
            self.reporter.increase_counter_time(used_cpu=True)
            # --- NUEVO: Loguear el PID ---
            self.reporter.log_execution(current_process.pid)
        else:
            # CPU Ocioso (Idle)
            print(f"[Tick {self.current_tick}] CPU Idle")
            self.reporter.increase_counter_time(used_cpu=False)
            # --- NUEVO: Loguear Idle (None) ---
            self.reporter.log_execution(None)

        # 4. Calcular métricas y avanzar reloj
        self.reporter.compute_metrics()
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
            self.tick()
            
            # Condición de parada: 
            # Si no hay procesos entrando Y todos los procesos registrados han terminado
            finished_count = len([p for p in self.reporter.processes.values() if p.is_finished()])
            total_count = len(self.reporter.processes)
            
            if not self.incoming_processes and finished_count == total_count:
                simulation_active = False

        print(self.reporter)