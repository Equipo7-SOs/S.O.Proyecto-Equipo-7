from .scheduler import Scheduler
from collections import deque

"""
    Implements First-Come, First-Served process scheduling 
    algorithm using a double ended queue.
"""
class FCFS(Scheduler):
    
    """
        Initializes the queue given a list of processes.
        It sorts them in ascending order by arrival time.
    """
    def __init__(self, processes=None):
        self.ready_queue = deque()
        self.current_process = None
        if processes:
            self.ready_queue = deque(sorted(processes, key=lambda x: x.arrival_time))

    """
    We'll assume the arrival time is greater than the previous ones.
    This is only for non-user generated simulations
    """
    def add_to_queue(self, new_process):
        self.ready_queue.append(new_process)

    """
    Chooses process to run during this tick
    """
    def choose_process(self):
        try:
            # We'll see if the current head has already been fully processed
            # or if there is no head hasn't been picked
            if self.current_process is None:
                self.current_process = self.ready_queue[0]
            elif self.current_process.remaining_time == 0:
                self.ready_queue.popleft() 
                self.current_process = self.ready_queue[0]
            # if the previous condition is not true then the head is still valid
        except IndexError: # the queue may run out of processes, if so we'll return None
            print("No more processes in queue")
            self.current_process = None
        finally:
            return self.current_process
    