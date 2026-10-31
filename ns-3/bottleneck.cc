// <--- How to run (./ns3 run "scratch/bottleneck --bottleneck=10Mbps") --->
// change the mbps as you want


#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    // Default bottleneck bandwidth
    std::string bottleneckRate = "10Mbps";

    CommandLine cmd;
    cmd.AddValue("bottleneck", "Bottleneck bandwidth", bottleneckRate);
    cmd.Parse(argc, argv);

    double simulationTime = 10.0;

    // Create four nodes
    NodeContainer nodes;
    nodes.Create(4);

    Ptr<Node> senderA = nodes.Get(0);
    Ptr<Node> senderB = nodes.Get(1);
    Ptr<Node> router = nodes.Get(2);
    Ptr<Node> receiver = nodes.Get(3);

    // Install Internet stack
    InternetStackHelper internet;
    internet.Install(nodes);

    // Configure access links
    PointToPointHelper accessLink;

    accessLink.SetDeviceAttribute(
        "DataRate", StringValue("100Mbps"));

    accessLink.SetChannelAttribute(
        "Delay", StringValue("2ms"));

    // Sender A to Router
    NetDeviceContainer devicesA =
        accessLink.Install(senderA, router);

    // Sender B to Router
    NetDeviceContainer devicesB =
        accessLink.Install(senderB, router);

    // Configure bottleneck link
    PointToPointHelper bottleneck;

    bottleneck.SetDeviceAttribute(
        "DataRate", StringValue(bottleneckRate));

    bottleneck.SetChannelAttribute(
        "Delay", StringValue("10ms"));

    // Small queue to observe packet drops
    bottleneck.SetQueue(
        "ns3::DropTailQueue<Packet>",
        "MaxSize", QueueSizeValue(QueueSize("10p")));

    // Router to Receiver
    NetDeviceContainer devicesR =
        bottleneck.Install(router, receiver);

    // Assign IP addresses
    Ipv4AddressHelper address;

    address.SetBase("10.1.1.0", "255.255.255.0");
    address.Assign(devicesA);

    address.SetBase("10.1.2.0", "255.255.255.0");
    address.Assign(devicesB);

    address.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer receiverInterfaces =
        address.Assign(devicesR);

    // Enable routing
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // UDP receiver
    uint16_t port = 5000;

    PacketSinkHelper sinkHelper(
        "ns3::UdpSocketFactory",
        InetSocketAddress(Ipv4Address::GetAny(), port));

    ApplicationContainer sinkApps =
        sinkHelper.Install(receiver);

    sinkApps.Start(Seconds(0.5));
    sinkApps.Stop(Seconds(simulationTime));

    // Sender A traffic
    OnOffHelper senderAApp(
        "ns3::UdpSocketFactory",
        InetSocketAddress(receiverInterfaces.GetAddress(1), port));

    senderAApp.SetAttribute(
        "DataRate", StringValue("8Mbps"));

    senderAApp.SetAttribute(
        "PacketSize", UintegerValue(1024));

    senderAApp.SetAttribute(
        "OnTime",
        StringValue("ns3::ConstantRandomVariable[Constant=1]"));

    senderAApp.SetAttribute(
        "OffTime",
        StringValue("ns3::ConstantRandomVariable[Constant=0]"));

    ApplicationContainer appA = senderAApp.Install(senderA);

    appA.Start(Seconds(1.0));
    appA.Stop(Seconds(9.0));

    // Sender B traffic
    OnOffHelper senderBApp(
        "ns3::UdpSocketFactory",
        InetSocketAddress(receiverInterfaces.GetAddress(1), port));

    senderBApp.SetAttribute(
        "DataRate", StringValue("8Mbps"));

    senderBApp.SetAttribute(
        "PacketSize", UintegerValue(1024));

    senderBApp.SetAttribute(
        "OnTime",
        StringValue("ns3::ConstantRandomVariable[Constant=1]"));

    senderBApp.SetAttribute(
        "OffTime",
        StringValue("ns3::ConstantRandomVariable[Constant=0]"));

    ApplicationContainer appB = senderBApp.Install(senderB);

    appB.Start(Seconds(1.0));
    appB.Stop(Seconds(9.0));

    // Install FlowMonitor
    FlowMonitorHelper flowHelper;
    Ptr<FlowMonitor> monitor = flowHelper.InstallAll();

    // Run simulation
    Simulator::Stop(Seconds(simulationTime));

    Simulator::Run();

    // Check packet losses
    monitor->CheckForLostPackets();

    Ptr<Ipv4FlowClassifier> classifier =
        DynamicCast<Ipv4FlowClassifier>(
            flowHelper.GetClassifier());

    FlowMonitor::FlowStatsContainer stats =
        monitor->GetFlowStats();

    std::cout << "\n===== BOTTLENECK RESULTS =====\n";
    std::cout << "Bottleneck bandwidth: "
              << bottleneckRate << "\n";

    for (auto iter = stats.begin(); iter != stats.end(); ++iter)
    {
        Ipv4FlowClassifier::FiveTuple t =
            classifier->FindFlow(iter->first);

        // Display UDP flows going to receiver port 5000
        if (t.protocol == 17 && t.destinationPort == port)
        {
            uint64_t txPackets = iter->second.txPackets;
            uint64_t rxPackets = iter->second.rxPackets;
            uint64_t lostPackets = iter->second.lostPackets;
            uint64_t rxBytes = iter->second.rxBytes;

            double throughput =
                (rxBytes * 8.0) / (8.0 * 1000000.0);

            double lossRatio = 0.0;

            if (txPackets > 0)
            {
                lossRatio =
                    (lostPackets * 100.0) / txPackets;
            }

            std::cout << "\nSource: "
                      << t.sourceAddress << "\n";

            std::cout << "Destination: "
                      << t.destinationAddress << "\n";

            std::cout << "Transmitted packets: "
                      << txPackets << "\n";

            std::cout << "Received packets: "
                      << rxPackets << "\n";

            std::cout << "Lost packets: "
                      << lostPackets << "\n";

            std::cout << "Packet loss ratio: "
                      << lossRatio << " %\n";

            std::cout << "Received bytes: "
                      << rxBytes << "\n";

            std::cout << "Throughput: "
                      << throughput << " Mbps\n";
        }
    }

    std::cout << "\n==============================\n";

    Simulator::Destroy();

    return 0;
}
