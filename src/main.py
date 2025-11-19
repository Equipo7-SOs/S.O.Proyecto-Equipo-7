from process import Process
from schedulers.fcfs import FCFS
from simulation import Simulation

processes = [
    Process(0, 0, 10),
    Process(1, 2, 3),
    Process(2, 5, 1),
    Process(3, 10, 2)
]

fcfs = FCFS(processes)
simulator = Simulation(fcfs, processes)

if __name__ == "__main__":
    simulator.simulate()