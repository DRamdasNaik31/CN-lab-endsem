
import org.arl.fjage.*
import org.arl.unet.sim.channels.*

// Select real-time simulation
platform = RealTimePlatform

// Configure ProtocolChannelModel
channel.model = ProtocolChannelModel
channel.communicationRange = 1500.m
channel.detectionRange = 2000.m
channel.interferenceRange = 2500.m

// Ensure deterministic communication
channel.pDetection = 1
channel.pDecoding = 1

println '''
Q1: Communication Range Using ProtocolChannelModel
==================================================
Node 1: Address 1, Position 0 m
Node 2: Address 2, Position 1200 m
Node 3: Address 3, Position 2400 m
'''

// Create three nodes
simulate {
    node 'Node1', address: 1,
         location: [0.m, 0.m, 0.m],
         web: 8081, api: 1101,
         stack: "$home/etc/setup"

    node 'Node2', address: 2,
         location: [1200.m, 0.m, 0.m],
         web: 8082, api: 1102,
         stack: "$home/etc/setup"

    node 'Node3', address: 3,
         location: [2400.m, 0.m, 0.m],
         web: 8083, api: 1103,
         stack: "$home/etc/setup"
}
