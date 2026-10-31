
from nest.topology import *

# Create two hosts and one router
h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")

# Connect h1 to router r1
eth1, etr1a = connect(h1, r1)

# Connect router r1 to h2
etr1b, eth2 = connect(r1, h2)

# Assign IP addresses
eth1.set_address("192.168.1.1/24")
etr1a.set_address("192.168.1.2/24")

etr1b.set_address("192.168.2.1/24")
eth2.set_address("192.168.2.2/24")

# Configure link attributes
eth1.set_attributes("5mbit", "5ms")
etr1a.set_attributes("10mbit", "100ms")

etr1b.set_attributes("5mbit", "5ms")
eth2.set_attributes("10mbit", "100ms")

# Add default routes to hosts
h1.add_route("DEFAULT", eth1, etr1a.address)
h2.add_route("DEFAULT", eth2, etr1b.address)

# Enable routing on router
r1.enable_ip_forwarding()

# Send five ping packets from h1 to h2
h1.ping(eth2.address, count=5)
