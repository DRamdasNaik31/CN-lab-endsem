
import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.phy.*

simulate {
    // Node A: address 10
    node 'A', address: 10,
         location: [0.m, 0.m, 0.m],
         web: 8081, api: 1101

    // Node B: address 20
    node 'B', address: 20,
         location: [1000.m, 0.m, 0.m],
         web: 8082, api: 1102
}
