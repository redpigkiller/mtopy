import numpy as np


def estimate_channel(yp, xp, Q, P, Nr, arg, flags):
    M = np.linalg.lstsq(arg['N'].T, P.T)
    x = xp[np.arange(1, M + 1) - 1]
    X_cir = circulant(x, arg['Lch'] + 1)
    Y_hat = np.reshape(yp, (M, None)).T
    
    if flags['estimate_dfo'] == 1:
        
        if Nr > 1:
            
            if strcmpi[flags['use_dfo_aoa_algo'] - 1, 'UNITARY_ESPRIT_2D' - 1]:
                eps_hat_q['theta_hat_q'] = unitaryesprit_2d(Y_hat, P, Q, flags['dfo_aoa_opt'])
                eps_hat_q = np.linalg.lstsq(eps_hat_q.T, M.T)
                theta_hat_q = np.linalg.lstsq((-theta_hat_q).T, arg['SP'].T)
                
                if flags['enable_sep'] != 0:
                    eps_q_max = np.linalg.lstsq((np.linalg.lstsq(arg['fc'].T, arg['fs'].T) @ np.linalg.lstsq(arg['v'].T, 3.6.T)).T, physconst['LightSpeed' - 1].T)
                    eps_hat_q = arrsepoptim(eps_hat_q, arg['dfo_gap'] @ eps_q_max)
                    theta_hat_q = arrsepoptim(theta_hat_q, arg['aoa_gap'])
            else:
                error['wrong algorithm selected' - 1]
        else:
            
            if strcmpi[flags['use_dfo_aoa_algo'] - 1, 'ESPRIT' - 1]:
                
                if flags['dfo_opt']['minus_mean'] == 0:
                    eps_hat_q['_'] = esprit(Y_hat, Q, flags['dfo_opt'])
                else:
                    eps_hat_q['_'] = esprit(Y_hat - mean[Y_hat - 1, 2 - 1], Q, flags['dfo_opt'])
                eps_hat_q = np.linalg.lstsq(eps_hat_q.T, M.T)
            elif strcmpi[flags['use_dfo_aoa_algo'] - 1, 'UNITARY_ESPRIT' - 1]:
                eps_hat_q['_'] = unitaryesprit(Y_hat, Q, flags['dfo_opt'])
                eps_hat_q = np.linalg.lstsq(eps_hat_q.T, M.T)
            elif strcmpi[flags['use_dfo_aoa_algo'] - 1, 'ML_Estimation' - 1]:
                eps_hat_q = ml_estimation(Y_hat, Q, flags['dfo_opt'], arg)
            else:
                error['wrong algorithm selected' - 1]
            
            if flags['enable_sep'] != 0:
                eps_q_max = np.linalg.lstsq((np.linalg.lstsq(arg['fc'].T, arg['fs'].T) @ np.linalg.lstsq(arg['v'].T, 3.6.T)).T, physconst['LightSpeed' - 1].T)
                eps_hat_q = arrsepoptim(eps_hat_q, arg['dfo_gap'] @ eps_q_max)
            theta_hat_q = np.zeros((Q, 1, 'like', yp))
    else:
        eps_hat_q = np.zeros((Q, 1, 'like', yp))
        theta_hat_q = np.zeros((Q, 1, 'like', yp))
    
    if flags['estimate_chl'] == 1:
        a_q1 = exp[-1j @ 2 @ pi @ arg['SP'] @ theta_hat_q @ np.arange(0, Nr - 1 + 1) - 1].T
        a_q2 = exp[1j @ 2 @ pi @ eps_hat_q @ M @ np.arange(0, P - 1 + 1) - 1].T
        A_hat = kr[a_q1 - 1, a_q2 - 1]
        
        if strcmpi[flags['use_chl_algo_stage_1'] - 1, 'PINV' - 1]:
            R_hat = np.linalg.lstsq(A_hat, Y_hat)
            R_hat = R_hat.T
        elif strcmpi[flags['use_chl_algo_stage_1'] - 1, 'TIKHONOV' - 1]:
            R_hat = np.linalg.lstsq(A_hat.conj().T @ A_hat + flags['chl_opt_stage_1']['reg'] @ eye[Q - 1, 'like' - 1, yp - 1], A_hat.conj().T) @ Y_hat
            R_hat = R_hat.T
        elif strcmpi[flags['use_chl_algo_stage_1'] - 1, 'PINV_KRON' - 1]:
            A_hat = kron[A_hat - 1, eye[M - 1, 'like' - 1, yp - 1] - 1]
            R_hat = np.linalg.lstsq(A_hat, yp)
            R_hat = np.reshape(R_hat, (M, None))
        elif strcmpi[flags['use_chl_algo_stage_1'] - 1, 'TIKHONOV_KRON' - 1]:
            A_hat = kron[A_hat - 1, eye[M - 1, 'like' - 1, yp - 1] - 1]
            R_hat = np.linalg.lstsq(A_hat.conj().T @ A_hat + flags['chl_opt_stage_1']['reg'] @ eye[Q - 1, 'like' - 1, yp - 1], A_hat.conj().T) @ yp
            R_hat = np.reshape(R_hat, (M, None))
        else:
            error['wrong algorithm selected' - 1]
        X_hat = np.zeros((Q, M, 'like', yp))
        
        for i_Q in np.arange(1, Q + 1):
            X_hat(i_Q, :) = diag[exp[-1j @ 2 @ pi @ eps_hat_q[i_Q - 1] @ np.arange(0, M - 1 + 1) - 1] - 1] @ R_hat[: - 1, i_Q - 1]
        
        if strcmpi[flags['use_chl_algo_stage_2'] - 1, 'PINV' - 1]:
            h_hat_q = np.linalg.lstsq(X_hat.T, X_cir.T.T)
        elif strcmpi[flags['use_chl_algo_stage_2'] - 1, 'MMSE' - 1]:
            h_hat_q = np.zeros((Q, arg['Lch'] + 1, 'like', yp))
            
            for i_Q in np.arange(1, Q + 1):
                xp_hat_q = X_hat[i_Q - 1, : - 1].T
                N0_xp = np.linalg.lstsq(abs[xp_hat_q.conj().T @ xp_hat_q - flags['chl_opt_stage_2']['chlpwr'] - 1].T, M.T)
                h_hat_q(i_Q, :) = np.linalg.lstsq(X_cir.conj().T.T, (X_cir @ X_cir.conj().T + N0_xp @ eye[M - 1]).T) @ xp_hat_q
        elif strcmpi[flags['use_chl_algo_stage_2'] - 1, 'CS' - 1]:
            h_hat_q = np.zeros((Q, arg['Lch'] + 1, 'like', yp))
            chllen = flags['chl_opt_stage_2']['chllen'] - 1
            n_delay = arg['Lch'] + 1 - chllen
            pinv_small_X_cir = cell[n_delay - 1, 1 - 1]
            
            for i_delay in np.arange(1, n_delay + 1):
                (pinv_small_X_cir, i_delay)[] = pinv[X_cir[: - 1, np.arange(i_delay, i_delay + chllen + 1) - 1] - 1]
            
            for i_Q in np.arange(1, Q + 1):
                xp_hat_q = X_hat[i_Q - 1, : - 1].T
                min_fval = inf
                min_delay = 0
                min_small_h_hat = np.zeros((chllen + 1, 1))
                
                for i_delay in np.arange(1, n_delay + 1):
                    small_h_hat = pinv_small_X_cir[i_delay - 1] @ xp_hat_q
                    fval = np.linalg.matrix_power(norm[xp_hat_q - X_cir[: - 1, np.arange(i_delay, i_delay + chllen + 1) - 1] @ small_h_hat - 1], 2)
                    
                    if min_fval > fval:
                        min_fval = fval
                        min_delay = i_delay
                        min_small_h_hat = small_h_hat
                h_hat_q(i_Q, [min_delay, min_delay + chllen]) = min_small_h_hat
        else:
            error['wrong algorithm selected' - 1]
    else:
        h_hat_q = np.zeros((Q, arg['Lch'] + 1, 'like', yp))
    return eps_hat_q[theta_hat_q][h_hat_q]