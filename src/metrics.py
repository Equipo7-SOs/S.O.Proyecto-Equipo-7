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

    # --- NUEVO MÉTODO 2: Imprimir el gráfico ---
    def print_gantt_chart(self):
        print(f"\n\t--- Gantt Chart: {self.name} ---")
        
        top_border = "  "
        middle_bar = "  "
        time_line  = "0 " 
        
        current_time = 0
        
        for entry in self.gantt_log:
            pid = entry['pid']
            duration = entry['duration']
            
            # Etiqueta: "P1" o "Idle"
            if pid is None:
                label = "Idle"
            else:
                label = f"P{pid}"
            
            block_width = max(len(label) + 2, duration + 2) 
            
            top_border += "_" * block_width
            
            padding = block_width - len(label)
            left_pad = padding // 2
            right_pad = padding - left_pad
            middle_bar += f"|{' ' * left_pad}{label}{' ' * right_pad}"
            
            current_time += duration
            
            time_str = str(current_time)

            # Espacios para llegar al final del bloque menos lo que ocupa el número
            space_needed = block_width - len(str(time_str)) + 1
            if len(time_line.split()[-1]) > 1: # Ajuste fino si el número anterior era largo
                 space_needed -= 1
            
            time_line += f"{' ' * (block_width - len(time_str))}{time_str} "

        top_border += "_" # Cerrar borde
        middle_bar += "|" # Cerrar barra
        
        print(top_border)
        print(middle_bar)
        print(top_border) 
        print(time_line)
        print("\n")

    def __str__(self):
        # Agregamos la llamada al Gantt aquí para que salga automático
        self.print_gantt_chart()
        
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