from abc import ABC, abstractmethod

"""
    Interface for all other scheduling algorithms
"""
class Scheduler(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def choose_process(self):
        pass

    def add_to_list(self, process):
        pass