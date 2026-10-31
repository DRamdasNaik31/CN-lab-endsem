
import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.net.*
import org.arl.unet.sim.channels.*

// Set this to false for the first run.
// Set it to true for the second run.
def enableRoutes = false

// Configure channel model
channel.model = ProtocolChannelModel
channel.communicationRange = 1000.m
channel.detectionRange = 1000.m
channel.interferenceRange = 1200.m
channel.pDetection = 1
channel.pDecoding = 1

println "Q5: Static Routing"
println "Communication range = 1000 m"
println "Node 11 = 0 m"
println "Node 12 = 800 m"
println "Node 13 = 1600 m"
println "Static routes enabled: ${enableRoutes}"

simulate {

    // Node 11
    def n11 = node 'Node11', address: 11,
        location: [0.m, 0.m, 0.m],
        web: 8081, api: 1101,
        stack: "$home/etc/setup"

    // Node 12 - intermediate router
    def n12 = node 'Node12', address: 12,
        location: [800.m, 0.m, 0.m],
        web: 8082, api: 1102,
        stack: "$home/etc/setup"

    // Node 13
    def n13 = node 'Node13', address: 13,
        location: [1600.m, 0.m, 0.m],
        web: 8083, api: 1103,
        stack: "$home/etc/setup"

    if (enableRoutes) {

        // Configure routes at Node 11 startup
        n11.startup = {
            def r = agentForService(Services.ROUTING)
            r << new EditRouteReq(
                op: RouteInfo.CREATE,
                to: 13,
                nextHop: 12
            )
            println "Node 11: Route to 13 via 12 configured"
        }

        // Configure forwarding and routes at Node 12 startup
        n12.startup = {
            def r = agentForService(Services.ROUTING)
            r.relay = true

            r << new EditRouteReq(
                op: RouteInfo.CREATE,
                to: 13,
                nextHop: 13
            )

            r << new EditRouteReq(
                op: RouteInfo.CREATE,
                to: 11,
                nextHop: 11
            )

            println "Node 12: Relay enabled"
        }

        // Configure route at Node 13 startup
        n13.startup = {
            def r = agentForService(Services.ROUTING)
            r << new EditRouteReq(
                op: RouteInfo.CREATE,
                to: 11,
                nextHop: 12
            )
            println "Node 13: Route to 11 via 12 configured"
        }
    }
}
