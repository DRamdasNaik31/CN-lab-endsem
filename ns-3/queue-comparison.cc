// <--- How to run (./ns3 run "scratch/queue-comparison --queue=DropTail") --->
// <--- How to run (./ns3 run "scratch/queue-comparison --queue=FqCoDel") --->

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    std::string queueType = "DropTail";

    CommandLine cmd;
    cmd.AddValue("queue", "Queue discipline: DropTail or FqCoDel",
                 queueType);
    cmd.Parse(argc, argv);

    if (queueType != "DropTail" && queueType != "FqCoDel")
    {
        std::cout << "Invalid queue type. Use DropTail or FqCoDel.\n";
        return 1;
    }

    // 1. Create nodes
    NodeContainer nodes;
    nodes.Create(3);

    Ptr<Node> sender = nodes.Get(0);
    Ptr<Node> router = nodes.Get(1);
    Ptr<Node> receiver = nodes.Get(2);

    // 2. Install Internet stack
    InternetStackHelper internet;
    internet.Install(nodes);

    // 3. Sender-to-router link
    PointToPointHelper accessLink;
    accessLink.SetDeviceAttribute(
        "DataRate", StringValue("100Mbps"));
    accessLink.SetChannelAttribute(
        "Delay", StringValue("2ms"));

    NetDeviceContainer accessDevices =
        accessLink.Install(sender, router);

    // 4. Router-to-receiver bottleneck link
    PointToPointHelper bottleneck;
    bottleneck.SetDeviceAttribute(
        "DataRate", StringValue("2Mbps"));
    bottleneck.SetChannelAttribute(
        "Delay", StringValue("10ms"));

    NetDeviceContainer bottleneckDevices =
        bottleneck.Install(router, receiver);

    // 5. Configure the outgoing queue at the router
    TrafficControlHelper trafficControl;

    if (queueType == "DropTail")
    {
        trafficControl.SetRootQueueDisc(
            "ns3::DropTailQueueDisc",
            "MaxSize",
            QueueSizeValue(QueueSize("100p")));
    }
    else
    {
        trafficControl.SetRootQueueDisc(
            "ns3::FqCoDelQueueDisc",
            "MaxSize",
            QueueSizeValue(QueueSize("100p")));
    }

    // Install queue discipline only on router's outgoing device
    NetDeviceContainer routerOutgoingDevice;
    routerOutgoingDevice.Add(bottleneckDevices.Get(0));

    QueueDiscContainer queueDiscs =
        trafficControl.Install(routerOutgoingDevice);

    // 6. Assign IP addresses
    Ipv4AddressHelper address;

    address.SetBase("10.1.1.0", "255.255.255.0");
    address.Assign(accessDevices);

    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer receiverInterfaces =
        address.Assign(bottleneckDevices);

    // 7. Enable routing
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // 8. Install UDP receiver
    uint16_t port = 5000;

    PacketSinkHelper sinkHelper(
        "ns3::UdpSocketFactory",
        InetSocketAddress(Ipv4Address::GetAny(), port));

    ApplicationContainer sinkApps = sinkHelper.Install(receiver);

    sinkApps.Start(Seconds(0.5));
    sinkApps.Stop(Seconds(11.0));

    // 9. Configure UDP sender
    OnOffHelper source(
        "ns3::UdpSocketFactory",
        InetSocketAddress(receiverInterfaces.GetAddress(1), port));

    source.SetAttribute(
        "DataRate", StringValue("20Mbps"));

    source.SetAttribute(
        "PacketSize", UintegerValue(1024));

    source.SetAttribute(
        "OnTime",
        StringValue("ns3::ConstantRandomVariable[Constant=1]"));

    source.SetAttribute(
        "OffTime",
        StringValue("ns3::ConstantRandomVariable[Constant=0]"));

    ApplicationContainer sourceApps = source.Install(sender);

    sourceApps.Start(Seconds(1.0));
    sourceApps.Stop(Seconds(9.0));

    // 10. Install FlowMonitor
    FlowMonitorHelper flowHelper;
    Ptr<FlowMonitor> monitor = flowHelper.InstallAll();

    // 11. Run simulation
    Simulator::Stop(Seconds(11.0));
    Simulator::Run();

    monitor->CheckForLostPackets();

    // 12. Collect flow statistics
    Ptr<Ipv4FlowClassifier> classifier =
        DynamicCast<Ipv4FlowClassifier>(
            flowHelper.GetClassifier());

    FlowMonitor::FlowStatsContainer stats =
        monitor->GetFlowStats();

    std::cout << "\n===== QUEUE DISCIPLINE RESULTS =====\n";
    std::cout << "Queue discipline: " << queueType << "\n";
    std::cout << "Bottleneck bandwidth: 2 Mbps\n";
    std::cout << "Sender offered rate: 20 Mbps\n";

    for (auto iter = stats.begin(); iter != stats.end(); ++iter)
    {
        Ipv4FlowClassifier::FiveTuple t =
            classifier->FindFlow(iter->first);

        if (t.protocol == 17 && t.destinationPort == port)
        {
            uint64_t txPackets = iter->second.txPackets;
            uint64_t rxPackets = iter->second.rxPackets;
            uint64_t lostPackets = iter->second.lostPackets;
            uint64_t rxBytes = iter->second.rxBytes;

            double throughput =
                (rxBytes * 8.0) / (8.0 * 1000000.0);

            double packetLoss = 0.0;
            if (txPackets > 0)
            {
                packetLoss =
                    (lostPackets * 100.0) / txPackets;
            }

            double averageDelay = 0.0;
            if (rxPackets > 0)
            {
                averageDelay =
                    (iter->second.delaySum.GetSeconds()
                     / rxPackets) * 1000.0;
            }

            std::cout << "\nPackets transmitted: "
                      << txPackets << "\n";

            std::cout << "Packets received: "
                      << rxPackets << "\n";

            std::cout << "Packets lost: "
                      << lostPackets << "\n";

            std::cout << "Packet loss ratio: "
                      << packetLoss << " %\n";

            std::cout << "Received bytes: "
                      << rxBytes << "\n";

            std::cout << "Throughput: "
                      << throughput << " Mbps\n";

            std::cout << "Average end-to-end delay: "
                      << averageDelay << " ms\n";
        }
    }

    std::cout << "\n====================================\n";

    Simulator::Destroy();

    return 0;
}
