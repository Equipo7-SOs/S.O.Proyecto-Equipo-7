class Metrics:
    def __init__(self, name):
        self.name = name
        self.processes = {} 
        self.cpu_use_time = 0 
        self.simulation_ticks = 0 
        
        # --- NUEVO: Historial de ejecución para el Gantt ---
        # Guardaremos tuplas: {'pid': id, 'duration': tiempo}
        self.gantt_log = [] 

        # Métricas finales
        self.throughput = 0.0
        self.avg_turnaround_time = 0.0
        self.avg_waiting_time = 0.0
        self.avg_response_time = 0.0
        self.cpu_utilization = 0.0

    def increase_counter_time(self, used_cpu=True):
        self.simulation_ticks += 1
        if used_cpu:
            self.cpu_use_time += 1

    def add_to_processes(self, p):
        self.processes[p.pid] = p

    def compute_metrics(self):
        finished_list = [p for p in self.processes.values() if p.is_finished()]
        count_finished = len(finished_list)

        if count_finished > 0:
            total_turnaround = sum(p.turnaround_time for p in finished_list)
            total_waiting = sum(p.waiting_time for p in finished_list)
            total_response = sum(p.response_time for p in finished_list)
            self.avg_turnaround_time = total_turnaround / count_finished
            self.avg_waiting_time = total_waiting / count_finished
            self.avg_response_time = total_response / count_finished
        
        if self.simulation_ticks > 0:
            self.throughput = count_finished / self.simulation_ticks
            self.cpu_utilization = (self.cpu_use_time / self.simulation_ticks) * 100

    def log_execution(self, pid):
        """
        Registra un tick de ejecución para el PID dado.
        Si el último registro es del mismo PID, simplemente aumentamos la duración.
        """
        if self.gantt_log and self.gantt_log[-1]['pid'] == pid:
            self.gantt_log[-1]['duration'] += 1
        else:
            self.gantt_log.append({'pid': pid, 'duration': 1})

    def __str__(self):
        
        return f"""
        --- Simulation Results: {self.name} ---
        Total Simulation Ticks:  {self.simulation_ticks}
        Total CPU Busy Time:     {self.cpu_use_time}
        CPU Utilization:         {self.cpu_utilization:.2f}%
        
        Processes Created:       {len(self.processes)}
        Processes Completed:     {len([p for p in self.processes.values() if p.is_finished()])}
        Throughput (proc/tick):  {self.throughput:.4f}
        
        Avg Turnaround Time:     {self.avg_turnaround_time:.2f}
        Avg Waiting Time:        {self.avg_waiting_time:.2f}
        Avg Response Time:       {self.avg_response_time:.2f}
        ---------------------------------------
        """
    def get_tick_log(self):
        """
        Expande gantt_log (con durations) a una lista donde cada índice es un tick 
        y el valor es el PID ejecutado en ese tick.
        """
        ticks = []
        for entry in self.gantt_log:
            pid = entry["pid"]
            duration = entry["duration"]
            ticks.extend([pid] * duration)
        return ticks
    
    # --- NUEVO MÉTODO 2: Imprimir el gráfico ---
    def print_compact_gantt(self):
        log = self.get_tick_log()   # << aquí convertimos
        
        if not log:
            print("No Gantt data.")
            return

        print(f"\n\n--- GANTT CHART: {self.name} ---")

        ranges = {}
        start = 0
        last = log[0]

        for i in range(1, len(log)+1):
            if i == len(log) or log[i] != last:
                ranges.setdefault(last, []).append((start, i))
                if i < len(log):
                    start = i
                    last = log[i]

        # ---- IMPRIMIR RESULTADOS ----
        for pid, segments in ranges.items():
            label = f"P{pid}" if pid is not None else "Idle"
            print(f"\n{label}:")
            for (s, e) in segments:
                print(f"  ticks {s} → {e}   (duración: {e - s})")
