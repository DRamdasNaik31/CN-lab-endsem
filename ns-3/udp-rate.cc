// <--- How to run (./ns3 run "scratch/udp-rate --rate=500kbps") --->
// Execute Run 2 (Above Link Capacity)
// Run with offered rate 2Mbps (Link capacity is 1Mbps)
// ./ns3 run "scratch/udp-rate --rate=2Mbps"

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("UdpRateScript");

int main (int argc, char *argv[])
{
  std::string DataRateStr = "500kbps"; // Default rate below capacity

  CommandLine cmd (__FILE__);
  cmd.AddValue ("rate", "Data rate of OnOffApplication", DataRateStr);
  cmd.Parse (argc, argv);

  // 1. Create 2 Nodes (UDP Sender and Receiver)
  NodeContainer nodes;
  nodes.Create (2);

  // 2. Configure Point-to-Point Link (Link Capacity = 1Mbps)
  PointToPointHelper p2p;
  p2p.SetDeviceAttribute ("DataRate", StringValue ("1Mbps"));
  p2p.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer devices;
  devices = p2p.Install (nodes);

  // 3. Install Internet Stack
  InternetStackHelper stack;
  stack.Install (nodes);

  // 4. Assign IP Addresses
  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  // 5. Install Packet Sink on Receiver (Node 1)
  uint16_t port = 9;
  Address sinkAddress (InetSocketAddress (interfaces.GetAddress (1), port));
  PacketSinkHelper packetSinkHelper ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), port));
  ApplicationContainer sinkApps = packetSinkHelper.Install (nodes.Get (1));
  sinkApps.Start (Seconds (1.0));
  sinkApps.Stop (Seconds (10.0));

  // 6. Install OnOffApplication on Sender (Node 0)
  OnOffHelper onoff ("ns3::UdpSocketFactory", sinkAddress);
  onoff.SetConstantRate (DataRate (DataRateStr));
  onoff.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer apps = onoff.Install (nodes.Get (0));
  apps.Start (Seconds (2.0));
  apps.Stop (Seconds (10.0));

  // 7. Install FlowMonitor to record packets
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  // 8. Run Simulation
  Simulator::Stop (Seconds (11.0));
  Simulator::Run ();

  // 9. Process Statistics
  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();

  for (auto i = stats.begin (); i != stats.end (); ++i)
    {
      Ipv4FlowProbeTag tag;
      std::cout << "\n--- Traffic Results for Rate: " << DataRateStr << " ---" << std::endl;
      std::cout << "Transmitted Packets (Sent) : " << i->second.txPackets << std::endl;
      std::cout << "Received Packets           : " << i->second.rxPackets << std::endl;
      std::cout << "Lost Packets               : " << i->second.lostPackets << std::endl;
      
      double pdr = ((double) i->second.rxPackets / i->second.txPackets) * 100.0;
      std::cout << "Packet Delivery Ratio (PDR): " << pdr << " %" << std::endl;
    }

  Simulator::Destroy ();
  return 0;
}