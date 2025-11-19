"""
Class that holds and compiles data of interest for the simulation
"""
class Metrics:

    def __init__(self):
        self.cpu_use_time = 0 # during how many ticks has a process been processed. Higher = better
        self.simulation_ticks = 0 # how many total ticks has the simulation run for. 
        #TODO implement this