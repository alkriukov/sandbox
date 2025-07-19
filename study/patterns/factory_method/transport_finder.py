from abc import ABC, abstractmethod

class TransportFinder(ABC):
    @abstractmethod
    def __init__(self): pass
    
    @abstractmethod
    def GetTransport(self): pass
