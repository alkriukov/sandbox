from transport_finder import TransportFinder
from truck import Truck

class TruckFinder(TransportFinder):
    def __init__(self): pass

    def GetTransport(self):
        return Truck()
