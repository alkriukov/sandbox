from transport_finder import TransportFinder
from boat import Boat

class BoatFinder(TransportFinder):
    def __init__(self): pass

    def GetTransport(self):
        return Boat()
