
from nest.topology import *

# Create six hosts
h1 = Node("h1")
h2 = Node("h2")
h3 = Node("h3")
h4 = Node("h4")
h5 = Node("h5")
h6 = Node("h6")

# Create two switches
s1 = Switch("s1")
s2 = Switch("s2")

# Connect LAN-1 hosts to switch s1
eth1, ets1a = connect(h1, s1)
eth2, ets1b = connect(h2, s1)
eth3, ets1c = connect(h3, s1)

# Connect LAN-2 hosts to switch s2
eth4, ets2a = connect(h4, s2)
eth5, ets2b = connect(h5, s2)
eth6, ets2c = connect(h6, s2)

# Connect the two switches
ets1d, ets2d = connect(s1, s2)

# Assign IP addresses to hosts
eth1.set_address("192.168.1.1/24")
eth2.set_address("192.168.1.2/24")
eth3.set_address("192.168.1.3/24")

eth4.set_address("192.168.1.4/24")
eth5.set_address("192.168.1.5/24")
eth6.set_address("192.168.1.6/24")

# Configure switch-to-switch link attributes
ets1d.set_attributes("100mbit", "1ms")
ets2d.set_attributes("100mbit", "1ms")

# Perform ping tests
h1.ping(eth4.address)
h2.ping(eth5.address)
h3.ping(eth6.address)
