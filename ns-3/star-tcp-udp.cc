// Throughput = (Received Bytes*8)/Simulation Duration
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    // Simulation time
    double simulationTime = 10.0;

    // Create four nodes
    NodeContainer nodes;
    nodes.Create(4);

    Ptr<Node> router = nodes.Get(0);
    Ptr<Node> sender1 = nodes.Get(1);
    Ptr<Node> sender2 = nodes.Get(2);
    Ptr<Node> receiver = nodes.Get(3);

    // Install Internet stack
    InternetStackHelper internet;
    internet.Install(nodes);

    // Configure point-to-point links
    PointToPointHelper p2p;

    p2p.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    p2p.SetChannelAttribute("Delay", StringValue("2ms"));

    // Connect router to sender 1
    NodeContainer link1(router, sender1);
    NetDeviceContainer devices1 = p2p.Install(link1);

    // Connect router to sender 2
    NodeContainer link2(router, sender2);
    NetDeviceContainer devices2 = p2p.Install(link2);

    // Connect router to receiver
    NodeContainer link3(router, receiver);
    NetDeviceContainer devices3 = p2p.Install(link3);

    // Assign IP addresses
    Ipv4AddressHelper address;

    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces1 =
        address.Assign(devices1);

    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces2 =
        address.Assign(devices2);

    address.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces3 =
        address.Assign(devices3);

    // Enable routing between networks
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // Application ports
    uint16_t tcpPort = 5000;
    uint16_t udpPort = 5001;

    // Install TCP receiver application
    PacketSinkHelper tcpSinkHelper(
        "ns3::TcpSocketFactory",
        InetSocketAddress(Ipv4Address::GetAny(), tcpPort)
    );

    ApplicationContainer tcpSinkApps =
        tcpSinkHelper.Install(receiver);

    tcpSinkApps.Start(Seconds(0.5));
    tcpSinkApps.Stop(Seconds(simulationTime));

    // Install UDP receiver application
    PacketSinkHelper udpSinkHelper(
        "ns3::UdpSocketFactory",
        InetSocketAddress(Ipv4Address::GetAny(), udpPort)
    );

    ApplicationContainer udpSinkApps =
        udpSinkHelper.Install(receiver);

    udpSinkApps.Start(Seconds(0.5));
    udpSinkApps.Stop(Seconds(simulationTime));

    // Configure TCP sender
    OnOffHelper tcpSender(
        "ns3::TcpSocketFactory",
        InetSocketAddress(interfaces3.GetAddress(1), tcpPort)
    );

    tcpSender.SetAttribute(
        "DataRate", StringValue("8Mbps")
    );

    tcpSender.SetAttribute(
        "PacketSize", UintegerValue(1024)
    );

    tcpSender.SetAttribute(
        "OnTime",
        StringValue("ns3::ConstantRandomVariable[Constant=1]")
    );

    tcpSender.SetAttribute(
        "OffTime",
        StringValue("ns3::ConstantRandomVariable[Constant=0]")
    );

    ApplicationContainer tcpSenderApps =
        tcpSender.Install(sender1);

    tcpSenderApps.Start(Seconds(1.0));
    tcpSenderApps.Stop(Seconds(9.0));

    // Configure UDP sender
    OnOffHelper udpSender(
        "ns3::UdpSocketFactory",
        InetSocketAddress(interfaces3.GetAddress(1), udpPort)
    );

    udpSender.SetAttribute(
        "DataRate", StringValue("8Mbps")
    );

    udpSender.SetAttribute(
        "PacketSize", UintegerValue(1024)
    );

    udpSender.SetAttribute(
        "OnTime",
        StringValue("ns3::ConstantRandomVariable[Constant=1]")
    );

    udpSender.SetAttribute(
        "OffTime",
        StringValue("ns3::ConstantRandomVariable[Constant=0]")
    );

    ApplicationContainer udpSenderApps =
        udpSender.Install(sender2);

    udpSenderApps.Start(Seconds(1.0));
    udpSenderApps.Stop(Seconds(9.0));

    // Run simulation
    Simulator::Stop(Seconds(simulationTime));

    Simulator::Run();

    // Get received bytes
    Ptr<PacketSink> tcpSink =
        DynamicCast<PacketSink>(tcpSinkApps.Get(0));

    Ptr<PacketSink> udpSink =
        DynamicCast<PacketSink>(udpSinkApps.Get(0));

    uint64_t tcpBytes = tcpSink->GetTotalRx();
    uint64_t udpBytes = udpSink->GetTotalRx();

    // Calculate throughput
    double duration = 8.0;

    double tcpThroughput =
        (tcpBytes * 8.0) / (duration * 1000000.0);

    double udpThroughput =
        (udpBytes * 8.0) / (duration * 1000000.0);

    // Display results
    std::cout << "\n===== STAR NETWORK RESULTS =====\n";

    std::cout << "\nTCP FLOW:\n";
    std::cout << "Bytes received = "
              << tcpBytes << " bytes\n";

    std::cout << "Throughput = "
              << tcpThroughput << " Mbps\n";

    std::cout << "\nUDP FLOW:\n";
    std::cout << "Bytes received = "
              << udpBytes << " bytes\n";

    std::cout << "Throughput = "
              << udpThroughput << " Mbps\n";

    std::cout << "\n================================\n";

    Simulator::Destroy();

    return 0;
}


// Throughput = (Received Bytes*8)/Simulation Duration