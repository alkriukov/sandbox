from abc import ABC, abstractmethod

class Transport(ABC):
    @abstractmethod
    def Deliver(self): pass
