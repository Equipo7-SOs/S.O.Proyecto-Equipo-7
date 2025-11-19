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
    def __init__(self, processes):
        self.ready_queue = deque(sorted(processes, key=lambda x: x.arrival_time))

    def __init__(self):
        self.ready_queue = deque()

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
            next_process = self.ready_queue.index(0)
            # if it has, we popleft and return the reference for the next process
            if next_process.remaining_time == 0:
                self.ready_queue.popleft()
                # once again we'll take the next process 
                next_process = self.ready_queue.index(0) # this one can't possibly have no remaining processing time 
        except IndexError: # the queue may run out of processes, if so we'll return None
            print("No more processes in queue")
            next_process = None
        finally:
            return next_process
    