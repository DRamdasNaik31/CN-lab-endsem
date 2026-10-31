
clc;
clear;
close all;

% Q2: Transmission Delay, Propagation Delay and Total Delay

%% Given Data

packetSize = 1500;             % Packet size in bytes
bandwidth = 10;                % Link bandwidth in Mbps
distance = 1200;               % Link distance in km
propagationSpeed = 2e8;        % Speed in metres/second
processingDelay = 2;           % Processing delay in milliseconds

%% 1. Calculate packet size in bits

packetBits = packetSize * 8;

fprintf('Packet size = %d bits\n', packetBits);

%% 2. Calculate transmission delay

bandwidth_bps = bandwidth * 1e6;

transmissionDelay = packetBits / bandwidth_bps;

transmissionDelay_ms = transmissionDelay * 1000;

fprintf('\nTransmission Delay:\n');
fprintf('In seconds = %.6f seconds\n', transmissionDelay);
fprintf('In milliseconds = %.3f ms\n', transmissionDelay_ms);

%% 3. Calculate propagation delay

distance_m = distance * 1000;

propagationDelay = distance_m / propagationSpeed;

propagationDelay_ms = propagationDelay * 1000;

fprintf('\nPropagation Delay:\n');
fprintf('Distance = %.0f metres\n', distance_m);
fprintf('In seconds = %.6f seconds\n', propagationDelay);
fprintf('In milliseconds = %.3f ms\n', propagationDelay_ms);

%% 4. Calculate total one-way delay

totalDelay = transmissionDelay_ms + ...
             propagationDelay_ms + ...
             processingDelay;

fprintf('\nTotal One-Way Delay = %.3f ms\n', totalDelay);

%% 5. Repeat calculations for different bandwidths

bandwidths = [5 10 20 50];

transmissionDelays = zeros(size(bandwidths));
totalDelays = zeros(size(bandwidths));

for i = 1:length(bandwidths)

    currentBandwidth = bandwidths(i) * 1e6;

    transmissionDelays(i) = ...
        (packetBits / currentBandwidth) * 1000;

    totalDelays(i) = transmissionDelays(i) + ...
                     propagationDelay_ms + ...
                     processingDelay;

end

%% Display Comparison Table

Results = table( ...
    bandwidths', ...
    transmissionDelays', ...
    repmat(propagationDelay_ms, length(bandwidths), 1), ...
    repmat(processingDelay, length(bandwidths), 1), ...
    totalDelays', ...
    'VariableNames', ...
    {'Bandwidth_Mbps', 'Transmission_ms', ...
     'Propagation_ms', 'Processing_ms', 'TotalDelay_ms'});

fprintf('\nComparison Table:\n');
disp(Results);

%% 6. Plot Bandwidth vs Total One-Way Delay

figure;

plot(bandwidths, totalDelays, '-o', ...
     'LineWidth', 2, 'MarkerSize', 8);

grid on;

xlabel('Bandwidth (Mbps)');
ylabel('Total One-Way Delay (ms)');

title('Bandwidth vs Total One-Way Delay');

% Display values near the points
for i = 1:length(bandwidths)
    text(bandwidths(i), totalDelays(i), ...
        sprintf(' %.2f ms', totalDelays(i)));
end

fprintf('\nObservation:\n');
fprintf(['As bandwidth increases, transmission delay decreases.\n' ...
         'However, total delay does not become zero because\n' ...
         'propagation and processing delays remain constant.\n']);
