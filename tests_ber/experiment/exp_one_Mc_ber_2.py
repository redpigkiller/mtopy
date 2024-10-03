import numpy as np


def exp_one_Mc_ber_2(i_Mc, sim_Mc_info, DEBUG):
    
    if nargin < 3:
        DEBUG = 0
    snr = sim_Mc_info['snr']
    Q = sim_Mc_info['Q']
    N = sim_Mc_info['config']['N']
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
    channel_data_idx['ii_Mc'] = segment_load[i_Mc - 1, 1 - 1]
    channel_data = load[sprintf['%s_%03d.mat' - 1, dir_gendata - 1, channel_data_idx - 1] - 1]
    estimat_data_idx['jj_Mc'] = segment_load[i_Mc - 1, 1 - 1]
    est_data = load[sprintf['%s_s_est_%03d.chl.mat' - 1, dir_estdata - 1, estimat_data_idx - 1] - 1]
    eps_Mc = channel_data['dfoVal']
    
    if np.ndim(eps_Mc) >= 3:
        eps_Mc = eps_Mc[: - 1, : - 1, ii_Mc - 1]
    h_Mc = channel_data['chlVal']
    
    if np.ndim(h_Mc) >= 3:
        h_Mc = h_Mc[: - 1, : - 1, ii_Mc - 1]
    eps_hat_Mc = est_data['est_dfoVal']
    
    if np.ndim(eps_hat_Mc) >= 3:
        eps_hat_Mc = eps_hat_Mc[: - 1, : - 1, jj_Mc - 1]
    h_hat_Mc = est_data['est_chlVal']
    
    if np.ndim(h_hat_Mc) >= 3:
        h_hat_Mc = h_hat_Mc[: - 1, : - 1, jj_Mc - 1]
    r_ber_Mc_n = np.zeros((n_Q, n_snr))
    r_ber_Mc_ml = np.zeros((n_Q, n_snr))
    
    for i_snr in np.arange(1, n_snr + 1):
        s_data = randi[np.array([[0, 1]]) - 1, n_data_block - 1, 2 @ N - 1]
        sigma_w = sqrt[np.linalg.lstsq(np.linalg.matrix_power(10.0, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T)).T, 2 .T) - 1]
        n_data = np.zeros((n_data_block, N, 'like', p_type))
        
        for i_block in np.arange(1, n_data_block + 1):
            n_data(i_block, :) = sigma_w * randn[N - 1, 1 - 1, 'like' - 1, p_type - 1] + 1j @ sigma_w * randn[N - 1, 1 - 1, 'like' - 1, p_type - 1]
        
        for i_Q in np.arange(1, n_Q + 1):
            eps_q = eps_Mc[Q_gendata_idx[i_Q - 1] - 1, snr_gendata_idx[i_snr - 1] - 1]
            h_q = h_Mc[Q_gendata_idx[i_Q - 1] - 1, snr_gendata_idx[i_snr - 1] - 1]
            eps_hat_q = eps_hat_Mc[Q_estchal_idx[i_Q - 1] - 1, snr_estchal_idx[i_snr - 1] - 1]
            h_hat_q = h_hat_Mc[Q_estchal_idx[i_Q - 1] - 1, snr_estchal_idx[i_snr - 1] - 1]
            
            if flag_use_gpu:
                eps_q = gpuArray[eps_q - 1]
            
            if flag_use_gpu:
                h_q = gpuArray[h_q - 1]
            
            if flag_use_gpu:
                eps_hat_q = gpuArray[eps_hat_q - 1]
            
            if flag_use_gpu:
                h_hat_q = gpuArray[h_hat_q - 1]
            n_trial_q = np.size(eps_q, 1)
            r_ber_trial_n = np.zeros((n_trial_q, n_data_block))
            r_ber_trial_ml = np.zeros((n_trial_q, n_data_block))
            
            for i_trial_q in np.arange(1, n_trial_q + 1):
                eps_q_trial = eps_q[i_trial_q - 1, : - 1].T
                h_q_trial = permute[h_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                eps_hat_q_trial = eps_hat_q[i_trial_q - 1, : - 1].T
                h_hat_q_trial = permute[h_hat_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                
                if sim_Mc_info['glob_flag']['use_correct_dfo'] @ 2 + sim_Mc_info['glob_flag']['use_correct_chl'] == 0:
                    chl_mtx = gen_channel_matrix[eps_hat_q_trial - 1, h_hat_q_trial - 1, N - 1]
                elif sim_Mc_info['glob_flag']['use_correct_dfo'] @ 2 + sim_Mc_info['glob_flag']['use_correct_chl'] == 1:
                    chl_mtx = gen_channel_matrix[eps_hat_q_trial - 1, h_q_trial - 1, N - 1]
                elif sim_Mc_info['glob_flag']['use_correct_dfo'] @ 2 + sim_Mc_info['glob_flag']['use_correct_chl'] == 2:
                    chl_mtx = gen_channel_matrix[eps_q_trial - 1, h_hat_q_trial - 1, N - 1]
                elif sim_Mc_info['glob_flag']['use_correct_dfo'] @ 2 + sim_Mc_info['glob_flag']['use_correct_chl'] == 3:
                    chl_mtx = gen_channel_matrix[eps_q_trial - 1, h_q_trial - 1, N - 1]
                else:
                    pass
                
                if algo_flag['null_subcarrier'] > 0:
                    
                    if algo_flag['position'] == 0:
                        chl_mtx = chl_mtx[: - 1, np.arange((algo_flag, 'null_subcarrier') + 1, end - (algo_flag, 'null_subcarrier') + 1) - 1]
                    else:
                        chl_mtx = chl_mtx[: - 1, [[1, np.linalg.lstsq(N.T, 2 .T) - (algo_flag, 'null_subcarrier') - 1], [np.linalg.lstsq(N.T, 2 .T) + (algo_flag, 'null_subcarrier') + 1, N]] - 1]
                yp_cell = cell[n_data_block - 1, 1 - 1]
                
                for i_block in np.arange(1, n_data_block + 1):
                    s_block = s_data[i_block - 1, : - 1].T
                    n_block = n_data[i_block - 1, : - 1].T
                    x_transmitted = nrSymbolModulate[s_block - 1, 'QPSK' - 1]
                    
                    if flag_use_gpu:
                        x_transmitted = gpuArray[x_transmitted - 1]
                    x_transmitted = sqrt[N - 1] @ ifft[x_transmitted - 1]
                    
                    if algo_flag['null_subcarrier'] > 0:
                        
                        if algo_flag['position'] == 0:
                            x_transmitted([1, (algo_flag, 'null_subcarrier')]) = 0
                            x_transmitted([end - (algo_flag, 'null_subcarrier') + 1, end]) = 0
                        else:
                            x_transmitted([np.linalg.lstsq(N.T, 2 .T) - (algo_flag, 'null_subcarrier'), np.linalg.lstsq(N.T, 2 .T) + (algo_flag, 'null_subcarrier')]) = 0
                    n_transmitted = n_block
                    
                    if flag_use_gpu:
                        n_transmitted = gpuArray[n_transmitted - 1]
                    rp = dfo_channel[x_transmitted - 1, n_transmitted - 1, eps_q_trial - 1, h_q_trial - 1, flag_add_noise - 1]
                    (yp_cell, i_block)[] = np.linalg.lstsq(1 .T, sqrt[N - 1].T) @ fft[rp - 1]
                
                if strcmpi[algo_flag['post'] - 1, 'ML_SEARCH' - 1]:
                    chl_mtx_post = ifft[fft[full[chl_mtx - 1] - 1] - 1, N - 1, 2 - 1]
                
                if strcmpi[algo_flag['equalizer'] - 1, 'ZF' - 1]:
                    
                    if strcmpi[algo_flag['post'] - 1, 'NONE' - 1]:
                        chl_mtx = ifft[fft[full[chl_mtx - 1] - 1] - 1, N - 1, 2 - 1]
                        pchl_mtx = inverse[chl_mtx - 1]
                    else:
                        pchl_mtx = inverse[chl_mtx_post - 1]
                elif strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1]:
                    
                    if algo_flag['equ_opt']['use_correct_snr'] == 1:
                        pchl_mtx = chl_mtx.conj().T @ inverse[full[chl_mtx @ chl_mtx.conj().T + np.linalg.matrix_power(10, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T)) @ speye[N - 1] - 1] - 1]
                        pchl_mtx = ifft[fft[pchl_mtx - 1] - 1, N - 1, 2 - 1]
                    elif algo_flag['equ_opt']['compute_snr_each_datablock'] == 0:
                        N0_yp = 0
                        
                        for i_block in np.arange(1, n_data_block + 1):
                            N0_yp = N0_yp + np.linalg.lstsq(abs[yp_cell[i_block - 1].conj().T @ yp_cell[i_block - 1] - np.linalg.matrix_power(norm[chl_mtx - 1, 'fro' - 1], 2) - 1].T, N.T)
                        N0_yp = np.linalg.lstsq(N0_yp.T, n_data_block.T)
                        pchl_mtx = chl_mtx.conj().T @ inverse[full[chl_mtx @ chl_mtx.conj().T + N0_yp @ speye[N - 1] - 1] - 1]
                        pchl_mtx = ifft[fft[pchl_mtx - 1] - 1, N - 1, 2 - 1]
                
                for i_block in np.arange(1, n_data_block + 1):
                    s_block = s_data[i_block - 1, : - 1].T
                    yp = yp_cell[i_block - 1]
                    
                    if strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1] and algo_flag['equ_opt']['compute_snr_each_datablock'] == 1:
                        N0_yp = np.linalg.lstsq(abs[yp.conj().T @ yp - np.linalg.matrix_power(norm[chl_mtx - 1, 'fro' - 1], 2) - 1].T, N.T)
                        pchl_mtx = chl_mtx.conj().T @ inverse[full[chl_mtx @ chl_mtx.conj().T + N0_yp @ speye[N - 1] - 1] - 1]
                        pchl_mtx = ifft[fft[pchl_mtx - 1] - 1, N - 1, 2 - 1]
                    ss_hat = pchl_mtx @ yp
                    s_hat_n = nrSymbolDemodulate[ss_hat - 1, 'QPSK' - 1, 'DecisionType' - 1, 'Hard' - 1]
                    s_hat_ml = ml_search(yp, ss_hat, chl_mtx_post, algo_flag['post_opt'])
                    
                    if algo_flag['null_subcarrier'] > 0:
                        
                        if algo_flag['position'] == 0:
                            s_block = s_block[np.arange(2 @ (algo_flag, 'null_subcarrier') + 1, end - 2 @ (algo_flag, 'null_subcarrier') + 1) - 1]
                        else:
                            s_block = s_block[[[1, N - 2 @ (algo_flag, 'null_subcarrier') - 2], [N + 2 @ (algo_flag, 'null_subcarrier') + 1, 2 @ N]] - 1]
                    ber_n = np.linalg.lstsq(biterr[s_block - 1, s_hat_n - 1].T, numel[s_block - 1].T)
                    ber_ml = np.linalg.lstsq(biterr[s_block - 1, s_hat_ml - 1].T, numel[s_block - 1].T)
                    r_ber_trial_n(i_trial_q, i_block) = ber_n
                    r_ber_trial_ml(i_trial_q, i_block) = ber_ml
            r_ber_Mc_n(i_Q, i_snr) = np.linalg.lstsq(sum[r_ber_trial_n - 1, 'all' - 1].T, numel[r_ber_trial_n - 1].T)
            r_ber_Mc_ml(i_Q, i_snr) = np.linalg.lstsq(sum[r_ber_trial_ml - 1, 'all' - 1].T, numel[r_ber_trial_ml - 1].T)
    return r_ber_Mc_n[r_ber_Mc_ml]