import numpy as np


def gen_dfo_aoa_channel_simple(Q, config, preset_var):
    T = np.linalg.lstsq(1.0.T, config['fs'].T)
    Q_max = max[Q - 1]
    n_Q = length[Q - 1]
    fd_q_max = np.linalg.lstsq((config['fc'] @ np.linalg.lstsq(config['v'].T, 3.6.T)).T, physconst['LightSpeed' - 1].T)
    dfo_cos_gap = config['dfo_gap']
    aoa_cos_gap = config['aoa_gap']
    
    if nargin < 3:
        DFOs = gen_angle(Q_max, dfo_cos_gap, -pi, pi)
        AOAs = gen_angle(Q_max, aoa_cos_gap, 0, pi)
        CHLs = randn[Q_max - 1, 1 - 1] + 1j @ randn[Q_max - 1, 1 - 1]
        CHLs = CHLs / abs[CHLs - 1]
        preset_var = struct
        preset_var['DFOs' - 1] = DFOs
        preset_var['AOAs' - 1] = AOAs
        preset_var['CHLs' - 1] = CHLs
    else:
        DFOs = preset_var['DFOs']
        AOAs = preset_var['AOAs']
        CHLs = preset_var['CHLs']
    CTNDs = sort[rand[Q_max - 1, 1 - 1] - 1]
    dfoVal = cell[n_Q - 1, 1 - 1]
    aoaVal = cell[n_Q - 1, 1 - 1]
    chlVal = cell[n_Q - 1, 1 - 1]
    
    for i_Q in np.arange(1, n_Q + 1):
        max_comb = nchoosek[Q_max - 1, Q[i_Q - 1] - 1]
        choose_comb = ceil[np.linalg.lstsq(Q_max.T, Q[i_Q - 1].T) - 1]
        n_trial_q = min[max_comb - 1, choose_comb - 1]
        DFOq = np.zeros((n_trial_q, Q[i_Q - 1]))
        AOAq = np.zeros((n_trial_q, Q[i_Q - 1]))
        CHLq = np.zeros((n_trial_q, Q[i_Q - 1], config['Lch'] + 1))
        repeated_selected_idx = np.zeros((n_trial_q, Q[i_Q - 1]))
        
        for i_trial_q in np.arange(1, n_trial_q + 1):
            selected_idx = sort[randsample[Q_max - 1, Q[i_Q - 1] - 1].T - 1]
            
            while ismember[selected_idx - 1, repeated_selected_idx - 1, 'rows' - 1]:
                selected_idx = sort[randsample[Q_max - 1, Q[i_Q - 1] - 1].T - 1]
            repeated_selected_idx(i_trial_q, :) = selected_idx
            selected_idx = selected_idx[randperm[Q[i_Q - 1] - 1] - 1]
            selected_dfo_q = DFOs[selected_idx - 1]
            selected_aoa_q = AOAs[selected_idx - 1]
            selected_CTND_q = CTNDs[selected_idx - 1]
            selected_CTP_q = get_CTP(selected_CTND_q, 1, config['pg_low'], config['pg_high'])
            selected_CHL_q = CHLs[selected_idx - 1]
            sigma_square = np.linalg.matrix_power(10.0, selected_CTP_q / 10)
            sigma_square = sigma_square / sum[sigma_square - 1]
            sigma = sqrt[sigma_square / 2 - 1]
            a0_q = sigma * selected_CHL_q
            tau_q = selected_CTND_q @ config['DS']
            fd_q = fd_q_max * cos[selected_dfo_q - 1]
            eps_q = fd_q @ T
            a_q = a0_q * exp[-1j @ 2 @ pi @ (config['fc'] + fd_q) * tau_q - 1]
            p_q = np.zeros((Q[i_Q - 1], config['Lch'] + 1))
            
            for ii_Q in np.arange(1, Q[i_Q - 1] + 1):
                
                for i_Lch in np.arange(0, (config, 'Lch') + 1):
                    p_q(ii_Q, i_Lch + 1) = rc_pulse((i_Lch - np.linalg.lstsq((config['H'] - 1).T, 2 .T)) @ T - tau_q[ii_Q - 1], T, config['H'], config['beta'])
            h_q = a_q * p_q
            DFOq(i_trial_q, :) = eps_q
            AOAq(i_trial_q, :) = cos[selected_aoa_q - 1]
            CHLq(i_trial_q, :, :) = h_q
        (dfoVal, i_Q)[] = DFOq
        (aoaVal, i_Q)[] = AOAq
        (chlVal, i_Q)[] = CHLq
    return dfoVal[aoaVal][chlVal][preset_var]


def get_CTP(CTND, CTND_max, lb, ub):
    
    if lb > ub:
        error['lower bound > upper bound' - 1]
    
    if any[(CTND[: - 1] < 0) - 1] or any[(CTND[: - 1] > 1) - 1]:
        error['CTND < 0 or CTND > 1' - 1]
    CTND = CTND / CTND_max
    CTP = ub - CTND @ (ub - lb)
    return CTP


def gen_angle(Q, gap, a, b):
    c_Q = 0
    phi = np.zeros((Q, 1))
    c_loop = 0
    
    while c_Q < Q:
        phi_q = a + (b - a) @ rand[1 - 1]
        
        if c_Q == 0:
            phi(1) = phi_q
            c_Q = c_Q + 1
        else:
            too_close_flag = 0
            idx = 1
            
            while idx <= c_Q:
                
                if abs[cos[phi_q - 1] - cos[phi[idx - 1] - 1] - 1] < gap:
                    too_close_flag = 1
                    
                    break
                idx = idx + 1
            
            if too_close_flag == 0:
                phi(c_Q + 1) = phi_q
                c_Q = c_Q + 1
        c_loop = c_loop + 1
        
        if c_loop > 1000:
            error['can not found!' - 1]
    return phi


def rc_pulse(t, T, H, beta):
    h = np.linalg.lstsq((H - 1).T, 2 .T)
    
    if abs[t - 1] > h @ T:
        value = 0
    else:
        
        if abs[t - 1] == np.linalg.lstsq(T.T, (2 @ beta).T):
            value = np.linalg.lstsq(pi.T, 4 .T) @ sinc[np.linalg.lstsq(1 .T, (2 @ beta).T) - 1]
        else:
            value = np.linalg.lstsq((sinc[np.linalg.lstsq(t.T, T.T) - 1] @ cos[np.linalg.lstsq((pi @ beta @ t).T, T.T) - 1]).T, (1 - np.linalg.matrix_power(np.linalg.lstsq((2 @ beta @ t).T, T.T), 2)).T)
    return value