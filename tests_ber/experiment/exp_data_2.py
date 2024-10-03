import numpy as np
import['ATLAB.Containers.Vecto' - 1]
flag_use_vec = 0
addpath[genpath['src' - 1] - 1]
sim_name = 'sim_03'
exp_name = 'exp_0322_0.9'
data_path = fullfile['_exp_dump_2' - 1, sim_name - 1, exp_name - 1]
Mc = 2000
Q = np.arange(1, 4 + 1)
snr = np.arange(10, 30 + 5, 5)
N = 1024
plot_snr = np.array([[0, 10, 20]])
subplot_snr = np.array([[3, 1]])
plot_Q = 1
n_Q = length[Q - 1]
n_snr = length[snr - 1]
ber_Mc_n = np.zeros((n_Q, n_snr, Mc))
ber_Mc_ml = np.zeros((n_Q, n_snr, Mc))
skip_collect = 0

if skip_collect == 0:
    
    for i_Mc in np.arange(1, Mc + 1):
        print(i_Mc)
        fname = sprintf['%s_r_avg_ber_%03d.ber.mat' - 1, sim_name - 1, i_Mc - 1]
        data = load[fullfile[data_path - 1, fname - 1] - 1]
        r_ber_Mc_n = data['r_ber_Mc_n']
        r_ber_Mc_ml = data['r_ber_Mc_ml']
        ber_Mc_n(:, :, i_Mc) = r_ber_Mc_n
        ber_Mc_ml(:, :, i_Mc) = r_ber_Mc_ml
    avg_ber_n = mean[ber_Mc_n - 1, 3 - 1]
    avg_ber_ml = mean[ber_Mc_ml - 1, 3 - 1]
cmap = np.array([['b', 'k', 'r', 'g', 'c', 'm', 'y']])
makr = np.array([['o', '+', '*', '.', 'x', '-']])
lins = np.array([['-', '--', ':', '-.']])

for q in np.arange(1, length[Q - 1] + 1):
    fig = figure[q - 1]
    semilogy[snr - 1, avg_ber_ml[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (MLE)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]
    semilogy[snr - 1, avg_ber_n[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (Original)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
    hold['f' - 1]
    xlabel['snr' - 1]
    ylabel['BER' - 1]
    title_str = sprintf['Q = %d' - 1, Q[q - 1] - 1]
    title[title_str - 1]
    grid['' - 1]
    legend['Location' - 1, 'southwest' - 1]