import numpy as np
sim_name = 'sim_release'
exp_name = 'exp_test_0222'
data_path = fullfile['_exp_dump' - 1, sim_name - 1, exp_name - 1]
Mc = 1
Q = np.arange(1, 4 + 1)
snr = np.arange(-10, 40 + 10, 10)
n_Q = length[Q - 1]
n_snr = length[snr - 1]
r_ZF_err_pt = cell[n_Q - 1, n_snr - 1]
r_ZF_cor_pt = cell[n_Q - 1, n_snr - 1]
r_ZF_err2_pt = cell[n_Q - 1, n_snr - 1]
r_ZF_cor2_pt = cell[n_Q - 1, n_snr - 1]
r_MMSE_err_pt = cell[n_Q - 1, n_snr - 1]
r_MMSE_cor_pt = cell[n_Q - 1, n_snr - 1]
r_MMSE_err2_pt = cell[n_Q - 1, n_snr - 1]
r_MMSE_cor2_pt = cell[n_Q - 1, n_snr - 1]
e_ZF = np.zeros((n_Q, n_snr))
e_MMSE = np.zeros((n_Q, n_snr))
e_CORR = np.zeros((n_Q, n_snr))

for i_Mc in np.arange(1, Mc + 1):
    i_Mc
    fname = sprintf['%s_r_avg_ber_%03d.ber.mat' - 1, sim_name - 1, i_Mc - 1]
    data = load[fullfile[data_path - 1, fname - 1] - 1]
    r_eZF_Mc = data['r_eZF_Mc']
    r_eMMSE_Mc = data['r_eMMSE_Mc']
    r_eCORR_Mc = data['r_eCORR_Mc']
    
    for i_Q in np.arange(1, n_Q + 1):
        
        for i_snr in np.arange(1, n_snr + 1):
            data_ZF = r_eZF_Mc[i_Q - 1, i_snr - 1]
            data_MMSE = r_eMMSE_Mc[i_Q - 1, i_snr - 1]
            data_CORR = r_eCORR_Mc[i_Q - 1, i_snr - 1]
            n_trial_q['n_block'] = np.shape(data_ZF)
            c1 = n_trial_q @ n_block
            ZFval = 0
            MMSEval = 0
            CORRval = 0
            ZF_err_pt = None
            ZF_cor_pt = None
            ZF_err2_pt = None
            ZF_cor2_pt = None
            MMSE_err_pt = None
            MMSE_cor_pt = None
            MMSE_err2_pt = None
            MMSE_cor2_pt = None
            
            for i_trial_q in np.arange(1, n_trial_q + 1):
                
                for i_block in np.arange(1, n_block + 1):
                    ZFval = ZFval + np.linalg.lstsq(1 .T, c1.T) @ (((data_ZF, n_trial_q, n_block),),)['val']
                    MMSEval = MMSEval + np.linalg.lstsq(1 .T, c1.T) @ (((data_MMSE, n_trial_q, n_block),),)['val']
                    CORRval = CORRval + np.linalg.lstsq(1 .T, c1.T) @ data_CORR[n_trial_q - 1, n_block - 1]
                    ZF_err_pt = np.array([[ZF_err_pt], [((((data_ZF, n_trial_q, n_block),),), 'err')]])
                    ZF_cor_pt = np.array([[ZF_cor_pt], [((((data_ZF, n_trial_q, n_block),),), 'cor')]])
                    ZF_err2_pt = np.array([[ZF_err2_pt], [((((data_ZF, n_trial_q, n_block),),), 'err2')]])
                    ZF_cor2_pt = np.array([[ZF_cor2_pt], [((((data_ZF, n_trial_q, n_block),),), 'cor2')]])
                    MMSE_err_pt = np.array([[MMSE_err_pt], [((((data_MMSE, n_trial_q, n_block),),), 'err')]])
                    MMSE_cor_pt = np.array([[MMSE_cor_pt], [((((data_MMSE, n_trial_q, n_block),),), 'cor')]])
                    MMSE_err2_pt = np.array([[MMSE_err2_pt], [((((data_MMSE, n_trial_q, n_block),),), 'err2')]])
                    MMSE_cor2_pt = np.array([[MMSE_cor2_pt], [((((data_MMSE, n_trial_q, n_block),),), 'cor2')]])
            e_ZF(i_Q, i_snr) = e_ZF[i_Q - 1, i_snr - 1] + ZFval
            e_MMSE(i_Q, i_snr) = e_MMSE[i_Q - 1, i_snr - 1] + MMSEval
            e_CORR(i_Q, i_snr) = e_CORR[i_Q - 1, i_snr - 1] + CORRval
            (r_ZF_err_pt, i_Q, i_snr)[] = np.array([[(((r_ZF_err_pt, i_Q, i_snr),),)], [ZF_err_pt]])
            (r_ZF_cor_pt, i_Q, i_snr)[] = np.array([[(((r_ZF_cor_pt, i_Q, i_snr),),)], [ZF_cor_pt]])
            (r_ZF_err2_pt, i_Q, i_snr)[] = np.array([[(((r_ZF_err2_pt, i_Q, i_snr),),)], [ZF_err2_pt]])
            (r_ZF_cor2_pt, i_Q, i_snr)[] = np.array([[(((r_ZF_cor2_pt, i_Q, i_snr),),)], [ZF_cor2_pt]])
            (r_MMSE_err_pt, i_Q, i_snr)[] = np.array([[(((r_MMSE_err_pt, i_Q, i_snr),),)], [MMSE_err_pt]])
            (r_MMSE_cor_pt, i_Q, i_snr)[] = np.array([[(((r_MMSE_cor_pt, i_Q, i_snr),),)], [MMSE_cor_pt]])
            (r_MMSE_err2_pt, i_Q, i_snr)[] = np.array([[(((r_MMSE_err2_pt, i_Q, i_snr),),)], [MMSE_err2_pt]])
            (r_MMSE_cor2_pt, i_Q, i_snr)[] = np.array([[(((r_MMSE_cor2_pt, i_Q, i_snr),),)], [MMSE_cor2_pt]])
e_ZF = np.linalg.lstsq(e_ZF.T, Mc.T)
e_MMSE = np.linalg.lstsq(e_MMSE.T, Mc.T)
e_CORR = np.linalg.lstsq(e_CORR.T, Mc.T)
cmap = np.array([['b', 'k', 'r', 'g', 'c', 'm', 'y']])
makr = np.array([['o', '+', '*', '.', 'x', '-']])
lins = np.array([['-', '--', ':', '-.']])
snr_plot[1 - 1, snr - 1, e_ZF - 1, Q - 1, 'snr' - 1, '' - 1, '' - 1]
fig = figure[2 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, e_ZF[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[3 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
legend['Location' - 1, 'southwest' - 1]

return
fig = figure[2 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, e_MMSE[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[3 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
legend['Location' - 1, 'southwest' - 1]
fig = figure[3 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, e_CORR[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[3 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
legend['Location' - 1, 'southwest' - 1]
ZF_err = np.zeros((n_Q, n_snr))
ZF_cor = np.zeros((n_Q, n_snr))
MMSE_err = np.zeros((n_Q, n_snr))
MMSE_cor = np.zeros((n_Q, n_snr))

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        ZF_err(i_Q, i_snr) = nan2zero[mean[r_ZF_err_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        ZF_cor(i_Q, i_snr) = nan2zero[mean[r_ZF_cor_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        MMSE_err(i_Q, i_snr) = nan2zero[mean[r_MMSE_err_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        MMSE_cor(i_Q, i_snr) = nan2zero[mean[r_MMSE_cor_pt[i_Q - 1, i_snr - 1] - 1] - 1]
fig = figure[4 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, ZF_err[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['error Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    semilogy[snr - 1, ZF_cor[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['correct Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
title['ZF' - 1]
legend['Location' - 1, 'southwest' - 1]
fig = figure[5 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, MMSE_err[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['error Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    semilogy[snr - 1, MMSE_cor[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['correct Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
title['MMSE' - 1]
legend['Location' - 1, 'southwest' - 1]
ZF_err2 = np.zeros((n_Q, n_snr))
ZF_cor2 = np.zeros((n_Q, n_snr))
MMSE_err2 = np.zeros((n_Q, n_snr))
MMSE_cor2 = np.zeros((n_Q, n_snr))

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        ZF_err2(i_Q, i_snr) = nan2zero[mean[r_ZF_err2_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        ZF_cor2(i_Q, i_snr) = nan2zero[mean[r_ZF_cor2_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        MMSE_err2(i_Q, i_snr) = nan2zero[mean[r_MMSE_err2_pt[i_Q - 1, i_snr - 1] - 1] - 1]
        MMSE_cor2(i_Q, i_snr) = nan2zero[mean[r_MMSE_cor2_pt[i_Q - 1, i_snr - 1] - 1] - 1]
fig = figure[6 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, ZF_err2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['error Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    semilogy[snr - 1, ZF_cor2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['correct Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
title['ZF' - 1]
legend['Location' - 1, 'southwest' - 1]
fig = figure[7 - 1]

for q in np.arange(1, length[Q - 1] + 1):
    semilogy[snr - 1, MMSE_err2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['error Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
    semilogy[snr - 1, MMSE_cor2[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([['correct Q=', str(Q[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[2 - 1] - 1, 'LineStyle' - 1, lins[2 - 1] - 1]
    hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
grid['' - 1]
title['MMSE' - 1]
legend['Location' - 1, 'southwest' - 1]

return
x_ZF_err_pt = [[]]
ZF_err_pt = None

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        nlen = length[r_ZF_cor_pt[i_Q - 1, i_snr - 1] - 1]
        
        if nlen == 0:
            
            continue
        Qlabel = repmat[str((i_snr - 1) @ n_Q + i_Q) - 1, nlen - 1, 1 - 1]
        x_ZF_err_pt = vertcat[x_ZF_err_pt - 1, cellstr[Qlabel - 1] - 1]
        ZF_err_pt = np.array([[ZF_err_pt], [(((r_ZF_cor_pt, i_Q, i_snr),),)]])
x_ZF_cor_pt = [[]]
ZF_cor_pt = None

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        nlen = length[r_ZF_cor_pt[i_Q - 1, i_snr - 1] - 1]
        
        if nlen == 0:
            
            continue
        Qlabel = repmat[str((i_snr - 1) @ n_Q + i_Q) - 1, nlen - 1, 1 - 1]
        x_ZF_cor_pt = vertcat[x_ZF_cor_pt - 1, cellstr[Qlabel - 1] - 1]
        ZF_cor_pt = np.array([[ZF_cor_pt], [(((r_ZF_cor_pt, i_Q, i_snr),),)]])
x1 = categorical[x_ZF_err_pt - 1]
x2 = categorical[x_ZF_cor_pt - 1]
figure[8 - 1]
scatter[x1 - 1, ZF_err_pt - 1, 10 - 1, 'red' - 1, 'filled' - 1]
hold['' - 1]
scatter[x2 - 1, ZF_cor_pt - 1, 10 - 1, 'blue' - 1, 'filled' - 1]
grid['' - 1]
hold['f' - 1]
x_MMSE_err_pt = [[]]
MMSE_err_pt = None

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        nlen = length[r_MMSE_err_pt[i_Q - 1, i_snr - 1] - 1]
        
        if nlen == 0:
            
            continue
        Qlabel = repmat[str((i_snr - 1) @ n_Q + i_Q) - 1, nlen - 1, 1 - 1]
        x_MMSE_err_pt = vertcat[x_MMSE_err_pt - 1, cellstr[Qlabel - 1] - 1]
        MMSE_err_pt = np.array([[MMSE_err_pt], [(((r_MMSE_err_pt, i_Q, i_snr),),)]])
x_MMSE_cor_pt = [[]]
MMSE_cor_pt = None

for i_snr in np.arange(1, n_snr + 1):
    
    for i_Q in np.arange(1, n_Q + 1):
        nlen = length[r_MMSE_cor_pt[i_Q - 1, i_snr - 1] - 1]
        
        if nlen == 0:
            
            continue
        Qlabel = repmat[str((i_snr - 1) @ n_Q + i_Q) - 1, nlen - 1, 1 - 1]
        x_MMSE_cor_pt = vertcat[x_MMSE_cor_pt - 1, cellstr[Qlabel - 1] - 1]
        MMSE_cor_pt = np.array([[MMSE_cor_pt], [(((r_MMSE_cor_pt, i_Q, i_snr),),)]])
x1 = categorical[x_MMSE_err_pt - 1]
x2 = categorical[x_MMSE_cor_pt - 1]
figure[9 - 1]
scatter[x1 - 1, MMSE_err_pt - 1, 10 - 1, 'red' - 1, 'filled' - 1]
hold['' - 1]
scatter[x2 - 1, MMSE_cor_pt - 1, 10 - 1, 'blue' - 1, 'filled' - 1]
grid['' - 1]
hold['f' - 1]