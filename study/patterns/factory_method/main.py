from boat_finder import BoatFinder
from client import Client

water_order = "Order #123"

boat_factory = BoatFinder()
client = Client()

client.ManageDelivery(water_order, boat_factory)
