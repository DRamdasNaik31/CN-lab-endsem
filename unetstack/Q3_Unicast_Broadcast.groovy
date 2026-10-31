
import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.sim.channels.*

channel.model = ProtocolChannelModel
channel.communicationRange = 1500.m

simulate {
    node 'Node1', address: 1,
         location: [0.m, 0.m, 0.m],
         web: 8081, api: 1101

    node 'Node2', address: 2,
         location: [500.m, 0.m, 0.m],
         web: 8082, api: 1102

    node 'Node3', address: 3,
         location: [1000.m, 0.m, 0.m],
         web: 8083, api: 1103
}
