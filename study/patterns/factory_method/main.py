from boat_finder import BoatFinder
from delivery_operator import DeliveryOperator

water_order = "Order #123"

boat_factory = BoatFinder()
operator = DeliveryOperator()

operator.ManageDelivery(water_order, boat_factory)
