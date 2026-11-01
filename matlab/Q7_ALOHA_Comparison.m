
clc;
clear;
close all;

% Q7: Pure ALOHA and Slotted ALOHA

%% 1. Generate G values

G = 0:0.05:3;

%% 2. Calculate normalized throughput

% Pure ALOHA
S_pure = G .* exp(-2 .* G);

% Slotted ALOHA
S_slotted = G .* exp(-G);

%% 3. Find maximum throughput

[maxPure, indexPure] = max(S_pure);
G_pure_max = G(indexPure);

[maxSlotted, indexSlotted] = max(S_slotted);
G_slotted_max = G(indexSlotted);

fprintf('PURE ALOHA:\n');
fprintf('Maximum Throughput = %.6f\n', maxPure);
fprintf('Corresponding G = %.2f\n', G_pure_max);

fprintf('\nSLOTTED ALOHA:\n');
fprintf('Maximum Throughput = %.6f\n', maxSlotted);
fprintf('Corresponding G = %.2f\n', G_slotted_max);

%% 4. Display throughput at selected G values

selectedG = [0.5 1.0 2.0];

pureValues = selectedG .* exp(-2 .* selectedG);
slottedValues = selectedG .* exp(-selectedG);

Results = table( ...
    selectedG', ...
    pureValues', ...
    slottedValues', ...
    'VariableNames', ...
    {'G', 'Pure_ALOHA', 'Slotted_ALOHA'});

fprintf('\nThroughput Comparison at Selected G Values:\n');
disp(Results);

%% 5. Plot both throughput curves

figure;

plot(G, S_pure, 'r-', 'LineWidth', 2);
hold on;

plot(G, S_slotted, 'b-', 'LineWidth', 2);

% Mark maximum throughput points
plot(G_pure_max, maxPure, 'ro', ...
    'MarkerSize', 8, 'MarkerFaceColor', 'r');

plot(G_slotted_max, maxSlotted, 'bo', ...
    'MarkerSize', 8, 'MarkerFaceColor', 'b');

grid on;

xlabel('Offered Load (G)');
ylabel('Normalized Throughput (S)');

title('Pure ALOHA vs Slotted ALOHA');

legend('Pure ALOHA', 'Slotted ALOHA', ...
       'Pure ALOHA Maximum', 'Slotted ALOHA Maximum', ...
       'Location', 'best');

hold off;

%% 6. Display comparison

fprintf('\nOBSERVATION:\n');

fprintf(['Slotted ALOHA achieves a higher maximum throughput ' ...
         'than Pure ALOHA.\n']);

fprintf(['Slotted ALOHA has a maximum throughput of 1/e, ' ...
         'while Pure ALOHA has a maximum throughput of 1/(2e).\n']);
