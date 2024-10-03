import numpy as np
import['ATLAB.Containers.Vecto' - 1]
flag_use_vec = 0
addpath[genpath['src' - 1] - 1]
sim_name = 'sim_release'
exp_name = 'exp_0224'
data_path = fullfile['_exp_dump' - 1, sim_name - 1, exp_name - 1]
Mc = 500
Q = np.arange(1, 4 + 1)
snr = np.arange(-10, 40 + 10, 10)
N = 1024
plot_snr = np.array([[0, 10, 20]])
subplot_snr = np.array([[3, 1]])
plot_Q = 1
thres_partition = 40
ratio_in_mean = np.linalg.lstsq(1 .T, 10 .T)
n_Q = length[Q - 1]
n_snr = length[snr - 1]
skip_collect = 1

if skip_collect == 0:
    e0_ZF_est = np.zeros((n_Q, n_snr, Mc))
    e0_ZF_idl = np.zeros((n_Q, n_snr, Mc))
    e0_MMSE_est = np.zeros((n_Q, n_snr, Mc))
    e0_MMSE_idl = np.zeros((n_Q, n_snr, Mc))
    e1_ZF_err_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e1_ZF_cor_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e1_MMSE_err_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e1_MMSE_cor_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e2_ZF_err_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e2_ZF_cor_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e2_MMSE_err_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    e2_MMSE_cor_pts = cell[n_Q - 1, n_snr - 1, Mc - 1]
    tic
    
    for i_Mc in np.arange(1, Mc + 1):
        print(i_Mc)
        fname = sprintf['%s_r_avg_ber_%03d.ber.mat' - 1, sim_name - 1, i_Mc - 1]
        data = load[fullfile[data_path - 1, fname - 1] - 1]
        r_eZF_Mc = data['r_eZF_Mc']
        r_eMMSE_Mc = data['r_eMMSE_Mc']
        
        for i_Q in np.arange(1, n_Q + 1):
            
            for i_snr in np.arange(1, n_snr + 1):
                data_ZF = r_eZF_Mc[i_Q - 1, i_snr - 1]
                data_MMSE = r_eMMSE_Mc[i_Q - 1, i_snr - 1]
                n_trial_q['n_block'] = np.shape(data_ZF)
                r_e0_ZF_est = 0
                r_e0_ZF_idl = 0
                r_e0_MMSE_est = 0
                r_e0_MMSE_idl = 0
                
                if flag_use_vec == 0:
                    r_e1_ZF_err_pts = None
                    r_e1_ZF_cor_pts = None
                    r_e1_MMSE_err_pts = None
                    r_e1_MMSE_cor_pts = None
                    r_e2_ZF_err_pts = None
                    r_e2_ZF_cor_pts = None
                    r_e2_MMSE_err_pts = None
                    r_e2_MMSE_cor_pts = None
                else:
                    pr_e1_ZF_err_pts = Vector[]
                    pr_e1_ZF_cor_pts = Vector[]
                    pr_e1_MMSE_err_pts = Vector[]
                    pr_e1_MMSE_cor_pts = Vector[]
                    pr_e2_ZF_err_pts = Vector[]
                    pr_e2_ZF_cor_pts = Vector[]
                    pr_e2_MMSE_err_pts = Vector[]
                    pr_e2_MMSE_cor_pts = Vector[]
                
                for i_trial_q in np.arange(1, n_trial_q + 1):
                    
                    for i_block in np.arange(1, n_block + 1):
                        r_e0_ZF_est = r_e0_ZF_est + (((data_ZF, i_trial_q, i_block),),)['e0_est']
                        r_e0_ZF_idl = r_e0_ZF_idl + (((data_ZF, i_trial_q, i_block),),)['e0_idl']
                        r_e0_MMSE_est = r_e0_MMSE_est + (((data_MMSE, i_trial_q, i_block),),)['e0_est']
                        r_e0_MMSE_idl = r_e0_MMSE_idl + (((data_MMSE, i_trial_q, i_block),),)['e0_idl']
                        
                        if flag_use_vec == 0:
                            r_e1_ZF_err_pts = np.array([[r_e1_ZF_err_pts], [((((data_ZF, i_trial_q, i_block),),), 'e1_err_pts')]])
                            r_e1_ZF_cor_pts = np.array([[r_e1_ZF_cor_pts], [((((data_ZF, i_trial_q, i_block),),), 'e1_cor_pts')]])
                            r_e1_MMSE_err_pts = np.array([[r_e1_MMSE_err_pts], [((((data_MMSE, i_trial_q, i_block),),), 'e1_err_pts')]])
                            r_e1_MMSE_cor_pts = np.array([[r_e1_MMSE_cor_pts], [((((data_MMSE, i_trial_q, i_block),),), 'e1_cor_pts')]])
                            r_e2_ZF_err_pts = np.array([[r_e2_ZF_err_pts], [((((data_ZF, i_trial_q, i_block),),), 'e2_err_pts')]])
                            r_e2_ZF_cor_pts = np.array([[r_e2_ZF_cor_pts], [((((data_ZF, i_trial_q, i_block),),), 'e2_cor_pts')]])
                            r_e2_MMSE_err_pts = np.array([[r_e2_MMSE_err_pts], [((((data_MMSE, i_trial_q, i_block),),), 'e2_err_pts')]])
                            r_e2_MMSE_cor_pts = np.array([[r_e2_MMSE_cor_pts], [((((data_MMSE, i_trial_q, i_block),),), 'e2_cor_pts')]])
                        else:
                            pr_e1_ZF_err_pts['PushBack'][(((data_ZF, i_trial_q, i_block),),)['e1_err_pts'] - 1]
                            pr_e1_ZF_cor_pts['PushBack'][(((data_ZF, i_trial_q, i_block),),)['e1_cor_pts'] - 1]
                            pr_e1_MMSE_err_pts['PushBack'][(((data_MMSE, i_trial_q, i_block),),)['e1_err_pts'] - 1]
                            pr_e1_MMSE_cor_pts['PushBack'][(((data_MMSE, i_trial_q, i_block),),)['e1_cor_pts'] - 1]
                            pr_e2_ZF_err_pts['PushBack'][(((data_ZF, i_trial_q, i_block),),)['e2_err_pts'] - 1]
                            pr_e2_ZF_cor_pts['PushBack'][(((data_ZF, i_trial_q, i_block),),)['e2_cor_pts'] - 1]
                            pr_e2_MMSE_err_pts['PushBack'][(((data_MMSE, i_trial_q, i_block),),)['e2_err_pts'] - 1]
                            pr_e2_MMSE_cor_pts['PushBack'][(((data_MMSE, i_trial_q, i_block),),)['e2_cor_pts'] - 1]
                e0_ZF_est(i_Q, i_snr, i_Mc) = np.linalg.lstsq(np.linalg.lstsq(r_e0_ZF_est.T, n_trial_q.T).T, n_block.T)
                e0_ZF_idl(i_Q, i_snr, i_Mc) = np.linalg.lstsq(np.linalg.lstsq(r_e0_ZF_idl.T, n_trial_q.T).T, n_block.T)
                e0_MMSE_est(i_Q, i_snr, i_Mc) = np.linalg.lstsq(np.linalg.lstsq(r_e0_MMSE_est.T, n_trial_q.T).T, n_block.T)
                e0_MMSE_idl(i_Q, i_snr, i_Mc) = np.linalg.lstsq(np.linalg.lstsq(r_e0_MMSE_idl.T, n_trial_q.T).T, n_block.T)
                
                if flag_use_vec == 0:
                    (e1_ZF_err_pts, i_Q, i_snr, i_Mc)[] = r_e1_ZF_err_pts
                    (e1_ZF_cor_pts, i_Q, i_snr, i_Mc)[] = r_e1_ZF_cor_pts
                    (e1_MMSE_err_pts, i_Q, i_snr, i_Mc)[] = r_e1_MMSE_err_pts
                    (e1_MMSE_cor_pts, i_Q, i_snr, i_Mc)[] = r_e1_MMSE_cor_pts
                    (e2_ZF_err_pts, i_Q, i_snr, i_Mc)[] = r_e2_ZF_err_pts
                    (e2_ZF_cor_pts, i_Q, i_snr, i_Mc)[] = r_e2_ZF_cor_pts
                    (e2_MMSE_err_pts, i_Q, i_snr, i_Mc)[] = r_e2_MMSE_err_pts
                    (e2_MMSE_cor_pts, i_Q, i_snr, i_Mc)[] = r_e2_MMSE_cor_pts
                else:
                    (e1_ZF_err_pts, i_Q, i_snr, i_Mc)[] = pr_e1_ZF_err_pts['Data']
                    (e1_ZF_cor_pts, i_Q, i_snr, i_Mc)[] = pr_e1_ZF_cor_pts['Data']
                    (e1_MMSE_err_pts, i_Q, i_snr, i_Mc)[] = pr_e1_MMSE_err_pts['Data']
                    (e1_MMSE_cor_pts, i_Q, i_snr, i_Mc)[] = pr_e1_MMSE_cor_pts['Data']
                    (e2_ZF_err_pts, i_Q, i_snr, i_Mc)[] = pr_e2_ZF_err_pts['Data']
                    (e2_ZF_cor_pts, i_Q, i_snr, i_Mc)[] = pr_e2_ZF_cor_pts['Data']
                    (e2_MMSE_err_pts, i_Q, i_snr, i_Mc)[] = pr_e2_MMSE_err_pts['Data']
                    (e2_MMSE_cor_pts, i_Q, i_snr, i_Mc)[] = pr_e2_MMSE_cor_pts['Data']
    fprintf['collecting time: %g\\n' - 1, toc - 1]
    e0_ZF_est = sum[e0_ZF_est - 1, 3 - 1] / Mc
    e0_ZF_idl = sum[e0_ZF_idl - 1, 3 - 1] / Mc
    e0_MMSE_est = sum[e0_MMSE_est - 1, 3 - 1] / Mc
    e0_MMSE_idl = sum[e0_MMSE_idl - 1, 3 - 1] / Mc
    mean_ZF_err1 = np.zeros((n_Q, n_snr))
    mean_ZF_cor1 = np.zeros((n_Q, n_snr))
    mean_MMSE_err1 = np.zeros((n_Q, n_snr))
    mean_MMSE_cor1 = np.zeros((n_Q, n_snr))
    e1_ZF_err_pts = cellcat[e1_ZF_err_pts - 1]
    e1_ZF_cor_pts = cellcat[e1_ZF_cor_pts - 1]
    e1_MMSE_err_pts = cellcat[e1_MMSE_err_pts - 1]
    e1_MMSE_cor_pts = cellcat[e1_MMSE_cor_pts - 1]
    
    for i_snr in np.arange(1, n_snr + 1):
        
        for i_Q in np.arange(1, n_Q + 1):
            mean_ZF_err1(i_Q, i_snr) = nan2zero[mean[e1_ZF_err_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_ZF_cor1(i_Q, i_snr) = nan2zero[mean[e1_ZF_cor_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_MMSE_err1(i_Q, i_snr) = nan2zero[mean[e1_MMSE_err_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_MMSE_cor1(i_Q, i_snr) = nan2zero[mean[e1_MMSE_cor_pts[i_Q - 1, i_snr - 1] - 1] - 1]
    mean_ZF_err2 = np.zeros((n_Q, n_snr))
    mean_ZF_cor2 = np.zeros((n_Q, n_snr))
    mean_MMSE_err2 = np.zeros((n_Q, n_snr))
    mean_MMSE_cor2 = np.zeros((n_Q, n_snr))
    e2_ZF_err_pts = cellcat[e2_ZF_err_pts - 1]
    e2_ZF_cor_pts = cellcat[e2_ZF_cor_pts - 1]
    e2_MMSE_err_pts = cellcat[e2_MMSE_err_pts - 1]
    e2_MMSE_cor_pts = cellcat[e2_MMSE_cor_pts - 1]
    
    for i_snr in np.arange(1, n_snr + 1):
        
        for i_Q in np.arange(1, n_Q + 1):
            mean_ZF_err2(i_Q, i_snr) = nan2zero[mean[e2_ZF_err_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_ZF_cor2(i_Q, i_snr) = nan2zero[mean[e2_ZF_cor_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_MMSE_err2(i_Q, i_snr) = nan2zero[mean[e2_MMSE_err_pts[i_Q - 1, i_snr - 1] - 1] - 1]
            mean_MMSE_cor2(i_Q, i_snr) = nan2zero[mean[e2_MMSE_cor_pts[i_Q - 1, i_snr - 1] - 1] - 1]
cmap = np.array([['b', 'k', 'r', 'g', 'c', 'm', 'y']])
makr = np.array([['o', '+', '*', '.', 'x', '-']])
lins = np.array([['-', '--', ':', '-.']])
close['l' - 1]
snr_plot[1 - 1, snr - 1, e0_ZF_est - 1, Q - 1, 'snr' - 1, '' - 1, 'ZF (estimation) e0' - 1]
snr_plot[2 - 1, snr - 1, e0_ZF_idl - 1, Q - 1, 'snr' - 1, '' - 1, 'ZF (ideal) e0' - 1]
snr_plot[3 - 1, snr - 1, e0_MMSE_est - 1, Q - 1, 'snr' - 1, '' - 1, 'MMSE (estimation) e0' - 1]
snr_plot[4 - 1, snr - 1, e0_MMSE_idl - 1, Q - 1, 'snr' - 1, '' - 1, 'MMSE (ideal) e0' - 1]
fig = figure[7 - 1]
pos = get[fig - 1, 'pos' - 1]
fig['Position' - 1] = pos

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, mean_ZF_err2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (error)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, mean_ZF_cor2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (correct)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
ylabel['value' - 1]
title['mean of ZF (e2)' - 1]
grid['' - 1]
legend['Location' - 1, 'southwest' - 1]
fig = figure[8 - 1]
pos = get[fig - 1, 'pos' - 1]
fig['Position' - 1] = pos

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, mean_MMSE_err2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (error)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, mean_MMSE_cor2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1]), ' (correct)']]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
ylabel['value' - 1]
title['mean of MMSE (e2)' - 1]
grid['' - 1]
legend['Location' - 1, 'southwest' - 1]
fig = figure[12 - 1]
pos = get[fig - 1, 'pos' - 1]
fig['Position' - 1] = np.array([[pos[1 - 1], pos[2 - 1] - 420, 560, 840]])

for idx in np.arange(1, length[plot_snr - 1] + 1):
    subplot[subplot_snr[1 - 1] - 1, subplot_snr[2 - 1] - 1, idx - 1]
    i_snr = find[(snr == plot_snr[idx - 1]) - 1]
    count_TP = np.zeros((n_Q, thres_partition))
    count_FN = np.zeros((n_Q, thres_partition))
    count_FP = np.zeros((n_Q, thres_partition))
    count_TN = np.zeros((n_Q, thres_partition))
    
    for i_Q in np.arange(1, n_Q + 1):
        
        if plot_Q > 0 and plot_Q != Q[i_Q - 1]:
            
            continue
        a = mean_MMSE_cor2[i_Q - 1, i_snr - 1]
        b = mean_MMSE_err2[i_Q - 1, i_snr - 1]
        
        if a > b:
            b['a'] = deal[a - 1, b - 1]
        thres_gap = np.linalg.lstsq((b - a).T, floor[thres_partition @ ratio_in_mean - 1].T)
        thres_lo_count = floor[np.linalg.lstsq((thres_partition - floor[thres_partition @ ratio_in_mean - 1]).T, 2 .T) - 1]
        thres_up_count = thres_partition - floor[thres_partition @ ratio_in_mean - 1] - thres_lo_count
        lb = a - thres_gap @ thres_lo_count
        
        if lb < 0:
            lb = 0
        ub = b + thres_gap @ thres_up_count
        lb = 0
        ub = 1
        thres = linspace[lb - 1, ub - 1, thres_partition - 1]
        
        for i_thres in np.arange(1, length[thres - 1] + 1):
            tot = length[e2_MMSE_cor_pts[i_Q - 1, i_snr - 1] - 1] + length[e2_MMSE_err_pts[i_Q - 1, i_snr - 1] - 1]
            
            if mod[tot - 1, N - 1] != 0:
                tot
                error['11' - 1]
            count_TP(i_Q, i_thres) = nnz[(e2_MMSE_err_pts[i_Q - 1, i_snr - 1] >= thres[i_thres - 1]) - 1]
            count_FN(i_Q, i_thres) = nnz[(e2_MMSE_err_pts[i_Q - 1, i_snr - 1] < thres[i_thres - 1]) - 1]
            count_FP(i_Q, i_thres) = nnz[(e2_MMSE_cor_pts[i_Q - 1, i_snr - 1] >= thres[i_thres - 1]) - 1]
            count_TN(i_Q, i_thres) = nnz[(e2_MMSE_cor_pts[i_Q - 1, i_snr - 1] < thres[i_thres - 1]) - 1]
    
    for i_Q in np.arange(1, n_Q + 1):
        
        if plot_Q > 0 and plot_Q != Q[i_Q - 1]:
            
            continue
        FNR = count_FN[i_Q - 1, : - 1] / (count_TP[i_Q - 1, : - 1] + count_FN[i_Q - 1, : - 1])
        FPR = count_FP[i_Q - 1, : - 1] / (count_FP[i_Q - 1, : - 1] + count_TN[i_Q - 1, : - 1])
        ACC = (count_TP[i_Q - 1, : - 1] + count_TN[i_Q - 1, : - 1]) / (count_TP[i_Q - 1, : - 1] + count_FN[i_Q - 1, : - 1] + count_FP[i_Q - 1, : - 1] + count_TN[i_Q - 1, : - 1])
        Precision = count_TP[i_Q - 1, : - 1] / (count_TP[i_Q - 1, : - 1] + count_FP[i_Q - 1, : - 1])
        Recall = count_TP[i_Q - 1, : - 1] / (count_TP[i_Q - 1, : - 1] + count_FN[i_Q - 1, : - 1])
        F1_score = 2 @ (Precision * Recall) / (Precision + Recall)
        semilogy[thres - 1, F1_score - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[i_Q - 1]), ' (F1_score)']]) - 1, 'Color' - 1, cmap[i_Q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
        hold['' - 1]
    hold['f' - 1]
    grid['' - 1]
    xlabel['threshold' - 1]
    ylabel['probabilty' - 1]
    title_str = sprintf['snr = %d MMSE (e2)' - 1, snr[i_snr - 1] - 1]
    title[title_str - 1]
    title_str = sprintf['Q = %d MMSE (e2)' - 1, plot_Q - 1]
    sgtitle[title_str - 1]
    legend['Location' - 1, 'southwest' - 1]