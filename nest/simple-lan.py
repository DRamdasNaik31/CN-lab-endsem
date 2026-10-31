from nest.topology import *

# Create four hosts
h1 = Node("h1")
h2 = Node("h2")
h3 = Node("h3")
h4 = Node("h4")

# Create switch
s1 = Switch("s1")


# Connect hosts to switch
eth1, ets1a = connect(h1, s1)
eth2, ets1b = connect(h2, s1)
eth3, ets1c = connect(h3, s1)
eth4, ets1d = connect(h4, s1)


# Assign IP addresses
eth1.set_address("192.168.1.1/24")
eth2.set_address("192.168.1.2/24")
eth3.set_address("192.168.1.3/24")
eth4.set_address("192.168.1.4/24")


# Configure bandwidth and delay
eth1.set_attributes("100mbit", "1ms")
eth2.set_attributes("100mbit", "1ms")
eth3.set_attributes("100mbit", "1ms")
eth4.set_attributes("100mbit", "1ms")


# Ping from h1 to h2
h1.ping(eth2.address)


# Ping from h3 to h4
h3.ping(eth4.address)