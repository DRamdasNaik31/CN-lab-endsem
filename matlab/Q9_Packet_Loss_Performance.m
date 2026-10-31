
clc;
clear;
close all;

% Q9: Packet Loss and Network Performance

%% 1. Input Data

packetNumbers = 1:10;

% 1 = Received, 0 = Lost
deliveryStatus = [1 1 1 0 1 1 0 1 1 1];

% NaN represents missing delay for lost packets
delays = [12 15 11 NaN 18 14 NaN 20 13 16];

%% 2. Calculate Packet Statistics

totalPackets = length(packetNumbers);

receivedPackets = sum(deliveryStatus == 1);
lostPackets = sum(deliveryStatus == 0);
transmittedPackets = totalPackets;

fprintf('NETWORK PERFORMANCE SUMMARY\n');
fprintf('----------------------------\n');

fprintf('Total transmitted packets = %d\n', transmittedPackets);
fprintf('Received packets = %d\n', receivedPackets);
fprintf('Lost packets = %d\n', lostPackets);

%% 3. Calculate Delivery and Loss Ratios

deliveryRatio = (receivedPackets / totalPackets) * 100;

lossRatio = (lostPackets / totalPackets) * 100;

fprintf('\nPacket Delivery Ratio = %.2f %%\n', deliveryRatio);
fprintf('Packet Loss Ratio = %.2f %%\n', lossRatio);

%% 4. Calculate Delay Statistics

% Select delays of received packets only
receivedDelays = delays(deliveryStatus == 1);

meanDelay = mean(receivedDelays);
medianDelay = median(receivedDelays);
minimumDelay = min(receivedDelays);
maximumDelay = max(receivedDelays);

fprintf('\nDELAY STATISTICS\n');
fprintf('----------------\n');

fprintf('Mean Delay = %.2f ms\n', meanDelay);
fprintf('Median Delay = %.2f ms\n', medianDelay);
fprintf('Minimum Delay = %.2f ms\n', minimumDelay);
fprintf('Maximum Delay = %.2f ms\n', maximumDelay);

%% 5. Display Packet Information Table

Results = table( ...
    packetNumbers', ...
    deliveryStatus', ...
    delays', ...
    'VariableNames', ...
    {'PacketNumber', 'DeliveryStatus', 'Delay_ms'});

fprintf('\nPACKET INFORMATION TABLE\n');
disp(Results);

%% 6. Plot Packet Number vs Measured Delay

figure;

% Plot received packets
receivedIndices = deliveryStatus == 1;

plot(packetNumbers(receivedIndices), ...
     delays(receivedIndices), 'bo-', ...
     'LineWidth', 1.5, 'MarkerSize', 8);

hold on;

% Mark lost packets separately at zero
lostIndices = deliveryStatus == 0;

plot(packetNumbers(lostIndices), ...
     zeros(1, sum(lostIndices)), 'rx', ...
     'MarkerSize', 12, 'LineWidth', 2);

grid on;

xlabel('Packet Number');
ylabel('Delay (ms)');

title('Packet Loss and Network Delay');

legend('Received Packets', 'Lost Packets', ...
       'Location', 'best');

xticks(1:10);

hold off;

%% 7. Observation

fprintf('\nOBSERVATION:\n');

fprintf(['Lost packets are represented using NaN because ' ...
         'their delay measurements are unavailable.\n']);

fprintf(['They must not be treated as zero-delay packets ' ...
         'because zero would incorrectly reduce the average delay.\n']);
