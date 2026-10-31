
clc;
clear;
close all;

% Q8: TCP Congestion Window Simulation

%% Given Parameters

initial_cwnd = 1;
ssthresh = 8;
totalRounds = 15;

% Create vectors
cwnd = zeros(1, totalRounds);
phase = strings(1, totalRounds);

% Initial congestion window
current_cwnd = initial_cwnd;

%% Simulate TCP Congestion Control

for round = 1:totalRounds

    % Store current congestion window
    cwnd(round) = current_cwnd;

    % Identify current phase
    if current_cwnd < ssthresh
        phase(round) = "Slow Start";
    else
        phase(round) = "Congestion Avoidance";
    end

    % Apply loss event after round 10
    if round == 10

        % Set new threshold to half current cwnd
        ssthresh = max(2, floor(current_cwnd / 2));

        % Reset cwnd for round 11
        current_cwnd = 1;

    else

        % Slow Start
        if current_cwnd < ssthresh
            current_cwnd = current_cwnd * 2;

        % Congestion Avoidance
        else
            current_cwnd = current_cwnd + 1;
        end

    end

end

%% Display Results

Rounds = (1:totalRounds)';

Results = table(Rounds, cwnd', phase', ...
    'VariableNames', {'Round', 'CongestionWindow', 'Phase'});

fprintf('\nTCP Congestion Window Table:\n');
disp(Results);

fprintf('Initial ssthresh = 8 segments\n');
fprintf('Loss event after round 10\n');
fprintf('New ssthresh = %d segments\n', ssthresh);

%% Plot Congestion Window

figure;

plot(Rounds, cwnd, '-o', ...
    'LineWidth', 2, 'MarkerSize', 7);

hold on;

% Mark loss event at round 10
xline(10, '--r', 'Loss Event', ...
    'LineWidth', 1.5);

% Label graph
xlabel('Round Number');
ylabel('Congestion Window (Segments)');

title('TCP Congestion Window Simulation');

grid on;

% Mark slow start and congestion avoidance phases
text(2, 5, 'Slow Start', 'FontSize', 10);
text(6, 12, 'Congestion Avoidance', 'FontSize', 10);
text(12, 5, 'Slow Start After Loss', 'FontSize', 10);

legend('Congestion Window', 'Loss Event', ...
    'Location', 'best');

hold off;
