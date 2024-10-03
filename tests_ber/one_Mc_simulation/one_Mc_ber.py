import numpy as np


def one_Mc_ber(i_Mc, sim_Mc_info):
    snr = sim_Mc_info['snr']
    Q = sim_Mc_info['Q']
    Nr = sim_Mc_info['Nr']
    N = sim_Mc_info['config']['N']
    SP = sim_Mc_info['config']['SP']
    add_CP_len = iif[sim_Mc_info['glob_flag']['enable_CP_sim'] - 1, sim_Mc_info['config']['Lcp'] - 1, 0 - 1]
    n_data_block = sim_Mc_info['config']['data_block']
    flag_use_gpu = sim_Mc_info['glob_flag']['use_gpu']
    flag_add_noise = sim_Mc_info['glob_flag']['add_noise']
    algo_flag = sim_Mc_info['algo_flag']
    dir_gendata = sim_Mc_info['dir_gendata']
    dir_estdata = sim_Mc_info['dir_estdata']
    snr_gendata_idx = sim_Mc_info['snr_gendata_idx']
    snr_estchal_idx = sim_Mc_info['snr_estchal_idx']
    Q_gendata_idx = sim_Mc_info['Q_gendata_idx']
    Q_estchal_idx = sim_Mc_info['Q_estchal_idx']
    n_snr = length[snr - 1]
    n_Q = length[Q - 1]
    
    if flag_use_gpu:
        p_type = np.zeros(('gpuArray',))
    else:
        p_type = np.zeros(())
    chl_data = load[sprintf['%s_%03d.mat' - 1, dir_gendata - 1, i_Mc - 1] - 1]
    est_data = load[sprintf['%s_est_%03d.est.mat' - 1, dir_estdata - 1, i_Mc - 1] - 1]
    dfoVal = chl_data['dfoVal']
    aoaVal = chl_data['aoaVal']
    chlVal = chl_data['chlVal']
    est_dfoVal = est_data['est_dfoVal']
    est_aoaVal = est_data['est_aoaVal']
    est_chlVal = est_data['est_chlVal']
    r_ber_Mc = np.zeros((n_Q, n_snr))
    
    for i_snr in np.arange(1, n_snr + 1):
        s_data = randi[np.array([[0, 1]]) - 1, n_data_block - 1, 2 @ N - 1]
        sigma_w = sqrt[np.linalg.lstsq(np.linalg.matrix_power(10.0, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T)).T, 2 .T) - 1]
        n_data = sigma_w * randn[n_data_block - 1, N @ Nr - 1, 'like' - 1, p_type - 1] + 1j @ sigma_w * randn[n_data_block - 1, N @ Nr - 1, 'like' - 1, p_type - 1]
        
        for i_Q in np.arange(1, n_Q + 1):
            dfo_q = dfoVal[Q_gendata_idx[i_Q - 1] - 1, snr_gendata_idx[i_snr - 1] - 1]
            aoa_q = aoaVal[Q_gendata_idx[i_Q - 1] - 1, snr_gendata_idx[i_snr - 1] - 1]
            chl_q = chlVal[Q_gendata_idx[i_Q - 1] - 1, snr_gendata_idx[i_snr - 1] - 1]
            dfo_hat_q = est_dfoVal[Q_estchal_idx[i_Q - 1] - 1, snr_estchal_idx[i_snr - 1] - 1]
            aoa_hat_q = est_aoaVal[Q_estchal_idx[i_Q - 1] - 1, snr_estchal_idx[i_snr - 1] - 1]
            chl_hat_q = est_chlVal[Q_estchal_idx[i_Q - 1] - 1, snr_estchal_idx[i_snr - 1] - 1]
            
            if flag_use_gpu:
                dfo_q = gpuArray[dfo_q - 1]
            
            if flag_use_gpu:
                aoa_q = gpuArray[aoa_q - 1]
            
            if flag_use_gpu:
                chl_q = gpuArray[chl_q - 1]
            
            if flag_use_gpu:
                dfo_hat_q = gpuArray[dfo_hat_q - 1]
            
            if flag_use_gpu:
                aoa_hat_q = gpuArray[aoa_hat_q - 1]
            
            if flag_use_gpu:
                chl_hat_q = gpuArray[chl_hat_q - 1]
            n_trial_q = np.size(dfo_q, 1)
            
            if (((n_trial_q != np.size(aoa_q, 1) or n_trial_q != np.size(chl_q, 1)) or n_trial_q != np.size(dfo_hat_q, 1)) or n_trial_q != np.size(aoa_hat_q, 1)) or n_trial_q != np.size(chl_hat_q, 1):
                error['unmatched # of trials' - 1]
            r_ber_trial = np.zeros((n_trial_q, n_data_block))
            
            for i_trial_q in np.arange(1, n_trial_q + 1):
                eps_q = dfo_q[i_trial_q - 1, : - 1].T
                theta_q = aoa_q[i_trial_q - 1, : - 1].T
                h_q = permute[chl_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                eps_hat_q = dfo_hat_q[i_trial_q - 1, : - 1].T
                theta_hat_q = aoa_hat_q[i_trial_q - 1, : - 1].T
                h_hat_q = permute[chl_hat_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                
                if sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 0:
                    chl_mtx = gen_channel_matrix[eps_hat_q - 1, theta_hat_q - 1, h_hat_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 1:
                    chl_mtx = gen_channel_matrix[eps_q - 1, theta_hat_q - 1, h_hat_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 2:
                    chl_mtx = gen_channel_matrix[eps_hat_q - 1, theta_q - 1, h_hat_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 3:
                    chl_mtx = gen_channel_matrix[eps_q - 1, theta_q - 1, h_hat_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 4:
                    chl_mtx = gen_channel_matrix[eps_hat_q - 1, theta_hat_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 5:
                    chl_mtx = gen_channel_matrix[eps_q - 1, theta_hat_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 6:
                    chl_mtx = gen_channel_matrix[eps_hat_q - 1, theta_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                elif sim_Mc_info['glob_flag']['gen_chl_mtx_flags'] == 7:
                    chl_mtx = gen_channel_matrix[eps_q - 1, theta_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, algo_flag - 1]
                else:
                    error['error gen_chl_mtx_flags' - 1]
                yp_cell = cell[n_data_block - 1, 1 - 1]
                
                for i_block in np.arange(1, n_data_block + 1):
                    s_block = s_data[i_block - 1, : - 1].T
                    n_block = n_data[i_block - 1, : - 1].T
                    x_transmitted = nrSymbolModulate[s_block - 1, 'QPSK' - 1]
                    
                    if flag_use_gpu:
                        x_transmitted = gpuArray[x_transmitted - 1]
                    x_transmitted = sqrt[N - 1] @ ifft[x_transmitted - 1]
                    n_transmitted = n_block
                    
                    if flag_use_gpu:
                        n_transmitted = gpuArray[n_transmitted - 1]
                    rp = dfo_channel_ula[x_transmitted - 1, n_transmitted - 1, eps_q - 1, theta_q - 1, h_q - 1, N - 1, Q[i_Q - 1] - 1, Nr - 1, SP - 1, flag_add_noise - 1, add_CP_len - 1]
                    (yp_cell, i_block)[] = rp
                flag_illcond = false
                
                if strcmpi[algo_flag['equalizer'] - 1, 'ZF' - 1]:
                    pchl_mtx = decomposition[chl_mtx - 1]
                    
                    if isIllConditioned[pchl_mtx - 1]:
                        flag_illcond = true
                        pchl_mtx = pinv[full[chl_mtx - 1] - 1]
                elif strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1]:
                    
                    if algo_flag['equ_opt']['use_correct_snr'] == 1:
                        pchl_mtx = np.linalg.lstsq(chl_mtx.conj().T.T, full[chl_mtx @ chl_mtx.conj().T + np.linalg.matrix_power(10, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T)) @ speye[N - 1] - 1].T)
                    elif algo_flag['equ_opt']['compute_snr_each_datablock'] == 0:
                        N0_yp = 0
                        
                        for i_block in np.arange(1, n_data_block + 1):
                            N0_yp = N0_yp + np.linalg.lstsq(np.linalg.lstsq(abs[yp_cell[i_block - 1].conj().T @ yp_cell[i_block - 1] - np.linalg.matrix_power(norm[chl_mtx - 1, 'fro' - 1], 2) - 1].T, N.T).T, Nr.T)
                        N0_yp = np.linalg.lstsq(N0_yp.T, n_data_block.T)
                        pchl_mtx = np.linalg.lstsq(chl_mtx.conj().T.T, full[chl_mtx @ chl_mtx.conj().T + N0_yp @ speye[N @ Nr - 1] - 1].T)
                
                for i_block in np.arange(1, n_data_block + 1):
                    s_block = s_data[i_block - 1, : - 1].T
                    yp = yp_cell[i_block - 1]
                    
                    if strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1] and algo_flag['equ_opt']['compute_snr_each_datablock'] == 1:
                        N0_yp = np.linalg.lstsq(abs[yp.conj().T @ yp - np.linalg.matrix_power(norm[chl_mtx - 1, 'fro' - 1], 2) - 1].T, N.T)
                        pchl_mtx = np.linalg.lstsq(chl_mtx.conj().T.T, full[chl_mtx @ chl_mtx.conj().T + N0_yp @ speye[N @ Nr - 1] - 1].T)
                    
                    if strcmpi[algo_flag['equalizer'] - 1, 'ZF' - 1]:
                        
                        if not flag_illcond:
                            ss_hat = np.linalg.lstsq(pchl_mtx, yp)
                        else:
                            ss_hat = pchl_mtx @ yp
                    elif strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1]:
                        ss_hat = pchl_mtx @ yp
                    ss_hat = np.linalg.lstsq(1 .T, sqrt[N - 1].T) @ fft[ss_hat - 1]
                    
                    if strcmpi[algo_flag['post'] - 1, 'NONE' - 1]:
                        s_hat = nrSymbolDemodulate[ss_hat - 1, 'QPSK' - 1, 'DecisionType' - 1, 'Hard' - 1]
                    elif strcmpi[algo_flag['post'] - 1, 'ML_SEARCH' - 1]:
                        s_hat = ml_search(yp, ss_hat, chl_mtx_post, algo_flag['post_opt'])
                    ber = np.linalg.lstsq(biterr[s_block - 1, s_hat - 1].T, numel[s_block - 1].T)
                    
                    if ber > 0.5:
                        ber = 0.5
                    r_ber_trial(i_trial_q, i_block) = ber
            r_ber_Mc(i_Q, i_snr) = np.linalg.lstsq(sum[r_ber_trial - 1, 'all' - 1].T, numel[r_ber_trial - 1].T)
    return r_ber_Mc