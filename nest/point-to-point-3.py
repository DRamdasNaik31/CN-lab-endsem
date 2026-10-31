from nest.topology import *

# Create hosts
h1 = Node("h1")
h2 = Node("h2")

# Create routers
r1 = Router("r1")
r2 = Router("r2")


# Connect h1 to r1
eth1, etr1a = connect(h1, r1)

# Connect r1 to r2
etr1b, etr2a = connect(r1, r2)

# Connect r2 to h2
etr2b, eth2 = connect(r2, h2)


# Assign IP addresses

# Network 1: 192.168.1.0/24
eth1.set_address("192.168.1.1/24")
etr1a.set_address("192.168.1.2/24")

# Network 2: 192.168.2.0/24
etr1b.set_address("192.168.2.1/24")
etr2a.set_address("192.168.2.2/24")

# Network 3: 192.168.3.0/24
etr2b.set_address("192.168.3.1/24")
eth2.set_address("192.168.3.2/24")


# Configure bandwidth and delay

# Link 1
eth1.set_attributes("5mbit", "5ms")
etr1a.set_attributes("10mbit", "100ms")

# Link 2
etr1b.set_attributes("5mbit", "5ms")
etr2a.set_attributes("10mbit", "100ms")

# Link 3
etr2b.set_attributes("5mbit", "5ms")
eth2.set_attributes("10mbit", "100ms")


# Configure default routes on hosts
h1.add_route("DEFAULT", eth1, etr1a.address)
h2.add_route("DEFAULT", eth2, etr2b.address)


# Configure routes on routers
r1.add_route("192.168.3.0/24", etr1b, etr2a.address)
r2.add_route("192.168.1.0/24", etr2a, etr1b.address)


# Ping from h1 to h2
h1.ping(eth2.address)