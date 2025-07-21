from transport_finder import TransportFinder
from transport import Transport

class Client():
    def __init__(self): pass
    
    def ManageDelivery(self, order, f: TransportFinder):
        print(f"Verifying {order}...")
        t: Transport = f.GetTransport()
        t.Deliver()
        print("Charging...")
        print("DONE\n")
