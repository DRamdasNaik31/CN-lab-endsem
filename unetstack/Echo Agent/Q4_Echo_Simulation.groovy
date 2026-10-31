
import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.sim.channels.*

channel.model = ProtocolChannelModel
channel.communicationRange = 1500.m

simulate {

    // Node 1
    node 'A', address: 1,
         location: [0.m, 0.m, 0.m],
         web: 8081, api: 1101

    // Node 2 with custom EchoAgent
    node 'B', address: 2,
         location: [1000.m, 0.m, 0.m],
         web: 8082, api: 1102,
         stack: {
             container.add 'arp',
                 new org.arl.unet.addr.AddressResolution()

             container.add 'mac',
                 new org.arl.unet.mac.CSMA()

             container.add 'uwlink',
                 new org.arl.unet.link.ECLink()

             container.add 'router',
                 new org.arl.unet.net.Router()

             container.add 'rdp',
                 new org.arl.unet.net.RouteDiscoveryProtocol()

             container.add 'caddy',
                 new org.arl.unet.transport.CaddyLite()

             container.add 'echo',
                 new EchoAgent()
         }
}
