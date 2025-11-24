from math import inf as infinity

class Process:

    def __init__(self, id, arrival_time, burst_time, priority=None):
        self.pid = id
        self.arrival_time = arrival_time # in which the process is introduced to ready q
        self.burst_time = burst_time # total processing time needed
        self.remaining_time = burst_time # remaining processing time needed
        self.priority = priority # process priority, not used by all scheduling algorithms
        self.turnaround_time = infinity 
        self.waiting_time = infinity
        self.completion_time = infinity
        self.response_time = infinity

    """
    Reports whether this process is finished
    """
    def is_finished(self):
        return self.remaining_time == 0

    """
    Waiting time: metric that tells process' duration in ready queue before 
    it begins executing. Lower is better.
    """
    def set_waiting_time(self):
        self.waiting_time = self.turnaround_time - self.burst_time
    
    """
    Turnaround time: time between when a process first arrives until it has 
    been completed. Lower is better.
    """
    def set_turnaround_time(self):
        self.turnaround_time = self.completion_time - self.arrival_time

    """
    Sets completion time for the process, also updates dependent metrics
    current_time: tick in which the process has finished processing
    """
    def set_completion_time(self, current_time):
        self.completion_time = current_time

    """
    Time between the process' arrival to the ready queue to when it is first executed.
    current_time: time in which it is first processed
    """
    def set_response_time(self, current_time):
        self.response_time = current_time - self.arrival_time

    """
    Updates the time the process needs to be finished processing, also updates other attributes 
    if the process has finished processing 
    processed_time: CPU time the process was given
    current_time: tick in which the process is being updated
    """
    def set_remaining_time(self, processed_time, current_time):
        # 1. Response Time: Se marca cuando el proceso EMPIEZA a ser atendido
        if self.remaining_time == self.burst_time:
            self.set_response_time(current_time)
        
        self.remaining_time -= processed_time
        
        # 2. Completion Time: Se marca cuando el proceso TERMINA.
        # Si estamos en el tick 0 y procesamos 1 unidad, terminamos en el tiempo 1.
        if self.remaining_time <= 0: # Usamos <= por seguridad
            self.remaining_time = 0
            self.set_completion_time(current_time + processed_time)
            
            self.set_turnaround_time()
            self.set_waiting_time()
