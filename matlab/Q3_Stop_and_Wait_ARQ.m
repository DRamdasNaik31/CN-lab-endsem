
clc;
clear;
close all;

% Q3: Stop-and-Wait ARQ Efficiency

%% Given Data

frameSize = 1000;           % Frame size in bytes
bandwidth = 4e6;            % Link bandwidth in bps
propagationDelay = 20;      % One-way propagation delay in ms

%% 1. Calculate Frame Transmission Time

frameBits = frameSize * 8;

transmissionTime = frameBits / bandwidth;

transmissionTime_ms = transmissionTime * 1000;

fprintf('Frame size = %d bits\n', frameBits);

fprintf('\nTransmission Time:\n');
fprintf('In seconds = %.6f seconds\n', transmissionTime);
fprintf('In milliseconds = %.3f ms\n', transmissionTime_ms);

%% 2. Calculate Round Trip Propagation Time

roundTripDelay = 2 * propagationDelay;

fprintf('\nRound Trip Propagation Time = %.2f ms\n', ...
        roundTripDelay);

%% 3. Calculate Stop-and-Wait Efficiency

efficiency = transmissionTime_ms / ...
             (transmissionTime_ms + roundTripDelay);

efficiency_percent = efficiency * 100;

fprintf('\nStop-and-Wait Efficiency = %.2f %%\n', ...
        efficiency_percent);

%% 4. Calculate Effective Throughput

bandwidth_Mbps = bandwidth / 1e6;

throughput = efficiency * bandwidth_Mbps;

fprintf('Effective Throughput = %.4f Mbps\n', throughput);

%% 5. Repeat for Different Propagation Delays

propagationDelays = [5 10 20 40 80];

roundTripDelays = 2 * propagationDelays;

efficiencies = transmissionTime_ms ./ ...
               (transmissionTime_ms + roundTripDelays);

efficiencies_percent = efficiencies * 100;

throughputs = efficiencies * bandwidth_Mbps;

%% Display Comparison Table

Results = table( ...
    propagationDelays', ...
    roundTripDelays', ...
    repmat(transmissionTime_ms, length(propagationDelays), 1), ...
    efficiencies_percent', ...
    throughputs', ...
    'VariableNames', ...
    {'PropagationDelay_ms', 'RoundTripDelay_ms', ...
     'TransmissionTime_ms', 'Efficiency_percent', ...
     'Throughput_Mbps'});

fprintf('\nComparison Table:\n');
disp(Results);

%% 6. Plot Propagation Delay vs Efficiency

figure;

plot(propagationDelays, efficiencies_percent, '-o', ...
     'LineWidth', 2, 'MarkerSize', 8);

grid on;

xlabel('One-Way Propagation Delay (ms)');
ylabel('Stop-and-Wait Efficiency (%)');

title('Propagation Delay vs Stop-and-Wait Efficiency');

for i = 1:length(propagationDelays)
    text(propagationDelays(i), efficiencies_percent(i), ...
        sprintf(' %.2f%%', efficiencies_percent(i)));
end

fprintf('\nObservation:\n');
fprintf(['As propagation delay increases, Stop-and-Wait efficiency ' ...
         'decreases because the sender spends more time waiting ' ...
         'for acknowledgements.\n']);
