Factory patterns allow high-level classes to create & use objects, depending only on Interfaces.
Otherwise they had to create objects with e.g. constructor. Therefore, depend on low-level class.

Factory Method pattern has Creator interface and concrete Creators, implementing it.
Create() method spawns a product instance. All concrete products implement Product interface.
Operator works only with Creator and Product interfaces. 

I __________        C __________        C __________        I _________
| Creator  |  <|--  | CreatorA |  --->  | ProductA |  --|>  | Product |
| Create() |        | Create() |        | Work()   |        | Work()  |
|          |        ------------        ------------        |         |
|          |                                                |         |
|          |        C __________        C __________        |         |
|          |  <|--  | CreatorB |  --->  | ProductA |  --|>  |         |    
|          |        | Create() |        | Work()   |        |         |
|          |        ------------        ------------        |         |
|          |                                                |         |
|          |           C ________________________           |         |
|          |  <------  | Client                 |  ------>  |         |
|          |           | HIGH-LEVEL-OPERATIONS  |           |         |
------------           --------------------------           -----------

EXAMPLE:
Product is Transport which can Deliver(). Boat and Truck implement transport.
Creator is TransportFinder, it can GetTransport(). Concrete creators are BoatFinder & TruckFinder.

Client (client.py) can ManageDelivery(). It makes high-level business operations:
Checks order, gets transport, executes delivery and charges the customer.
It DOES NOT CARE on exact transport or concrete factory.

main.py represents e.g. port delivery subsystem. It handles orders that need delivery by water.
If we need a road hub delivery subsystem, its structure will be like main.py, just with trucks.

RUN:
python3 main.py
Verifying Order #123...
Getting Boat
Delivering by Boat
Charging...
DONE

