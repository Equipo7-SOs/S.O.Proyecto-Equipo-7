"""
Class that runs a simulation, takes a list of processes and a scheduling 
algorithm and simulates an execution of a CPU scheduling
"""

class Simulation:

    def __init__(self, scheduler, processes=[]):
        self.current_tick = 0 # we'll simulate time discretely in integer ticks
        self.scheduler = scheduler # chosen cpu scheduler algorithm
        self.processes = processes # list of processes, can be user-given or empty
        self.generate_processes = True if processes is [] else False
        self.gantt_data = [] # Data for a Gantt table, which process ran at which time 

    """
    Generates a list of random processes if a list is not provided by the user
    number_of_processes: amount of processes the user wants to have generated
    desired_runtime: sum of the total amounts of burst time for all processes, approximately
    """
    def generate_processes(self, number_of_processes, desired_runtime):
        # TODO: implement
        print("hola")

    """
    Runs one tick of the simulation, the current process is given one tick of processing time 
    and if the algorithm calls for it another one is queued, or the simulation is ended if 
    there are no more processes
    """
    def tick(self):
        current_process = self.scheduler.choose_process() # returns either None or something
        if current_process:
            current_process.set_remaining_time(1, self.current_tick) # processing current
            print(f"Process with ID {current_process.pid} processed during tick {self.current_tick}")
            # TODO update metrics
            return True
        return False

    """
    Main loop of the simulation, runs until all processes are finished
    """
    def simulate(self):
        processes_remain = True
        while processes_remain:
            processes_remain = self.tick()