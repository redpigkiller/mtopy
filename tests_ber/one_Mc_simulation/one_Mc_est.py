import numpy as np


def one_Mc_est(i_Mc, sim_Mc_info, skip_Q, skip_snr):
    
    if nargin < 3:
        skip_Q = None
        skip_snr = None
    elif nargin < 4:
        skip_snr = None
    snr = sim_Mc_info['snr']
    Q = sim_Mc_info['Q']
    Nr = sim_Mc_info['Nr']
    P = sim_Mc_info['P']
    N = sim_Mc_info['config']['N']
    SP = sim_Mc_info['config']['SP']
    Lch = sim_Mc_info['config']['Lch']
    add_CP_len = iif[sim_Mc_info['glob_flag']['enable_CP_sim'] - 1, sim_Mc_info['config']['Lcp'] - 1, 0 - 1]
    flag_use_gpu = sim_Mc_info['glob_flag']['use_gpu']
    flag_add_noise = sim_Mc_info['glob_flag']['add_noise']
    algo_flag = sim_Mc_info['algo_flag']
    dir_gendata = sim_Mc_info['dir_gendata']
    snr_idx = sim_Mc_info['snr_idx']
    Q_idx = sim_Mc_info['Q_idx']
    M = np.linalg.lstsq(N.T, P.T)
    n_snr = length[snr - 1]
    n_Q = length[Q - 1]
    
    if flag_use_gpu:
        p_type = np.zeros(('gpuArray',))
    else:
        p_type = np.zeros(())
    chl_data = load[sprintf['%s_%03d.mat' - 1, dir_gendata - 1, i_Mc - 1] - 1]
    dfoVal = chl_data['dfoVal']
    aoaVal = chl_data['aoaVal']
    chlVal = chl_data['chlVal']
    r_MSE_dfo = np.zeros((n_Q, n_snr))
    r_MSE_aoa = np.zeros((n_Q, n_snr))
    r_MSE_chl = np.zeros((n_Q, n_snr))
    s_est_dfo = cell[n_Q - 1, n_snr - 1]
    s_est_aoa = cell[n_Q - 1, n_snr - 1]
    s_est_chl = cell[n_Q - 1, n_snr - 1]
    
    for i_snr in np.arange(1, n_snr + 1):
        s_training = randi[np.array([[0, 1]]) - 1, 2 @ M - 1, 1 - 1]
        x_training = nrSymbolModulate[s_training - 1, 'QPSK' - 1]
        x_training = sqrt[M - 1] @ ifft[x_training - 1]
        
        if flag_use_gpu:
            x_training = gpuArray[x_training - 1]
        x_training = repmat[x_training - 1, P - 1, 1 - 1]
        sigma_w = sqrt[np.linalg.lstsq(np.linalg.matrix_power(10.0, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T)).T, 2 .T) - 1]
        n_training = sigma_w * randn[N @ Nr - 1, 1 - 1, 'like' - 1, p_type - 1] + 1j @ sigma_w * randn[N @ Nr - 1, 1 - 1, 'like' - 1, p_type - 1]
        
        for i_Q in np.arange(1, n_Q + 1):
            
            if ismember[snr[i_snr - 1] - 1, skip_snr - 1] and ismember[Q[i_Q - 1] - 1, skip_Q - 1]:
                
                continue
            dfo_q = dfoVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            aoa_q = aoaVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            chl_q = chlVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            
            if flag_use_gpu:
                dfo_q = gpuArray[dfo_q - 1]
            
            if flag_use_gpu:
                aoa_q = gpuArray[aoa_q - 1]
            
            if flag_use_gpu:
                chl_q = gpuArray[chl_q - 1]
            r_MSE_dfo_trial = 0
            r_MSE_aoa_trial = 0
            r_MSE_chl_trial = 0
            n_trial_q = np.size(dfo_q, 1)
            
            if n_trial_q != np.size(aoa_q, 1) or n_trial_q != np.size(chl_q, 1):
                error['unmatched # of trials' - 1]
            s_est_dfo_trial = np.zeros((n_trial_q, Q[i_Q - 1]))
            s_est_aoa_trial = np.zeros((n_trial_q, Q[i_Q - 1]))
            s_est_chl_trial = np.zeros((n_trial_q, Q[i_Q - 1], Lch + 1))
            
            for i_trial_q in np.arange(1, n_trial_q + 1):
                eps_q = dfo_q[i_trial_q - 1, : - 1].T
                theta_q = aoa_q[i_trial_q - 1, : - 1].T
                h_q = permute[chl_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                rp = dfo_channel_ula[x_training - 1, n_training - 1, eps_q - 1, theta_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, flag_add_noise - 1, add_CP_len - 1]
                eps_hat_q['theta_hat_q']['h_hat_q'] = estimate_channel[rp - 1, x_training - 1, Q[i_Q - 1] - 1, P - 1, Nr - 1, sim_Mc_info['config'] - 1, algo_flag - 1]
                eps_hat_q['pair_Ind'] = arrpair[eps_q - 1, eps_hat_q - 1, 0.5 - 1]
                theta_hat_q = theta_hat_q[pair_Ind - 1]
                h_hat_q = h_hat_q[pair_Ind - 1, : - 1]
                s_est_dfo_trial(i_trial_q, :) = eps_hat_q
                s_est_aoa_trial(i_trial_q, :) = theta_hat_q
                s_est_chl_trial(i_trial_q, :, :) = h_hat_q[: - 1, np.arange(1, Lch + 1 + 1) - 1]
                MSE_eps = np.linalg.lstsq(np.linalg.matrix_power(norm[circdist[eps_hat_q - 1, eps_q - 1, 0.5 - 1, true - 1] - 1], 2).T, Q[i_Q - 1].T)
                MSE_theta = np.linalg.lstsq(np.linalg.matrix_power(norm[circdist[theta_hat_q - 1, theta_q - 1, 1 - 1, true - 1] - 1], 2).T, Q[i_Q - 1].T)
                mean_MSE_h_q = np.linalg.lstsq(np.linalg.matrix_power(norm[h_hat_q[: - 1, np.arange(1, Lch + 1 + 1) - 1] - h_q[: - 1, np.arange(1, Lch + 1 + 1) - 1] - 1, 'fro' - 1], 2).T, Q[i_Q - 1].T)
                r_MSE_dfo_trial = r_MSE_dfo_trial + MSE_eps
                r_MSE_aoa_trial = r_MSE_aoa_trial + MSE_theta
                r_MSE_chl_trial = r_MSE_chl_trial + mean_MSE_h_q
            (s_est_dfo, i_Q, i_snr)[] = s_est_dfo_trial
            (s_est_aoa, i_Q, i_snr)[] = s_est_aoa_trial
            (s_est_chl, i_Q, i_snr)[] = s_est_chl_trial
            r_MSE_dfo(i_Q, i_snr) = np.linalg.lstsq(r_MSE_dfo_trial.T, n_trial_q.T)
            r_MSE_aoa(i_Q, i_snr) = np.linalg.lstsq(r_MSE_aoa_trial.T, n_trial_q.T)
            r_MSE_chl(i_Q, i_snr) = np.linalg.lstsq(r_MSE_chl_trial.T, n_trial_q.T)
    return r_MSE_dfo[r_MSE_aoa][r_MSE_chl][s_est_dfo][s_est_aoa][s_est_chl]