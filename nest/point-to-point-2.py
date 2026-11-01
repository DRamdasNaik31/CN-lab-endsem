from nest.topology import *

h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")  

eth1, etr1a = connect(h1, r1)
etr1b, eth2 = connect(r1, h2)

eth1.set_address("192.168.1.1/24")
etr1a.set_address("192.168.1.2/24")

etr1b.set_address("192.168.2.1/24")
eth2.set_address("192.168.2.2/24")


eth1.set_attributes("5mbit", "5ms") 
etr1b.set_attributes("5mbit", "5ms")  


eth2.set_attributes("10mbit", "100ms")
etr1a.set_attributes("10mbit", "100ms") 

h1.add_route("DEFAULT", eth1)
h2.add_route("DEFAULT", eth2)

h1.ping(eth2.address)