import numpy as np


def one_Mc_crb(i_Mc, sim_Mc_info, skip_Q, skip_snr):
    
    if nargin < 3:
        skip_Q = None
        skip_snr = None
    elif nargin < 4:
        skip_snr = None
    snapshots_factor = 1
    snr = sim_Mc_info['snr']
    Q = sim_Mc_info['Q']
    Nr = sim_Mc_info['Nr']
    P = sim_Mc_info['P']
    N = sim_Mc_info['config']['N']
    SP = sim_Mc_info['config']['SP']
    dir_gendata = sim_Mc_info['dir_gendata']
    snr_idx = sim_Mc_info['snr_idx']
    Q_idx = sim_Mc_info['Q_idx']
    M = np.linalg.lstsq(N.T, P.T)
    n_snr = length[snr - 1]
    n_Q = length[Q - 1]
    eps_q_max = np.linalg.lstsq((np.linalg.lstsq(sim_Mc_info['config']['fc'].T, sim_Mc_info['config']['fs'].T) @ np.linalg.lstsq(sim_Mc_info['config']['v'].T, 3.6.T)).T, physconst['LightSpeed' - 1].T)
    chl_data = load[sprintf['%s_%03d.mat' - 1, dir_gendata - 1, i_Mc - 1] - 1]
    dfoVal = chl_data['dfoVal']
    aoaVal = chl_data['aoaVal']
    chlVal = chl_data['chlVal']
    r_dfo_crb = np.zeros((n_Q, n_snr))
    r_aoa_crb = np.zeros((n_Q, n_snr))
    
    for i_snr in np.arange(1, n_snr + 1):
        x_training = cell[snapshots_factor - 1, 1 - 1]
        
        for ii in np.arange(1, snapshots_factor + 1):
            s = randi[np.array([[0, 1]]) - 1, 2 @ M - 1, 1 - 1]
            x = nrSymbolModulate[s - 1, 'QPSK' - 1]
            x = sqrt[M - 1] @ ifft[x - 1]
            (x_training, ii)[] = repmat[x - 1, P - 1, 1 - 1]
        
        for i_Q in np.arange(1, n_Q + 1):
            
            if ismember[snr[i_snr - 1] - 1, skip_snr - 1] and ismember[Q[i_Q - 1] - 1, skip_Q - 1]:
                
                continue
            dfo_q = dfoVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            aoa_q = aoaVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            chl_q = chlVal[Q_idx[i_Q - 1] - 1, snr_idx[i_snr - 1] - 1]
            r_dfo_crb_trial = 0
            r_aoa_crb_trial = 0
            n_trial_q = np.size(dfo_q, 1)
            
            if n_trial_q != np.size(aoa_q, 1) or n_trial_q != np.size(chl_q, 1):
                error['unmatched # of trials' - 1]
            
            for i_trial_q in np.arange(1, n_trial_q + 1):
                eps_q = dfo_q[i_trial_q - 1, : - 1].T
                theta_q = aoa_q[i_trial_q - 1, : - 1].T
                h_q = permute[chl_q[i_trial_q - 1, : - 1, : - 1] - 1, np.array([[2, 3, 1]]) - 1]
                
                if Nr == 1:
                    theta_q = np.zeros((Q[i_Q - 1], 1))
                B = cell[Q[i_Q - 1] - 1, 1 - 1]
                
                for jj in np.arange(1, Q[i_Q - 1] + 1):
                    (B, jj)[] = exp[2j @ pi @ eps_q[jj - 1] - 1] @ circulant[h_q[jj - 1, : - 1].T - 1, M - 1]
                Rx = np.zeros((Q[i_Q - 1],))
                
                for jj in np.arange(1, Q[i_Q - 1] + 1):
                    
                    for kk in np.arange(jj, Q[i_Q - 1] + 1):
                        Rx(jj, kk) = np.linalg.lstsq(1 .T, M.T) @ trace[B[jj - 1] @ B[kk - 1].conj().T - 1]
                    
                    for kk in np.arange(1, jj - 1 + 1):
                        Rx(jj, kk) = conj[Rx[kk - 1, jj - 1] - 1]
                noise_var = np.linalg.matrix_power(10, np.linalg.lstsq((-snr[i_snr - 1]).T, 10 .T))
                
                if Nr == 1:
                    A = exp[1j @ 2 @ pi @ eps_q @ M @ np.arange(0, P - 1 + 1) - 1].T
                    D = 1j @ 2 @ pi @ M @ np.arange(0, P - 1 + 1).T * A
                else:
                    a_q1 = exp[-1j @ 2 @ pi @ SP @ theta_q @ np.arange(0, Nr - 1 + 1) - 1].T
                    a_q2 = exp[1j @ 2 @ pi @ eps_q @ M @ np.arange(0, P - 1 + 1) - 1].T
                    A = kr[a_q1 - 1, a_q2 - 1]
                    D1 = kr[(-1j @ 2 @ pi @ SP @ np.arange(0, Nr - 1 + 1)).T * a_q1 - 1, a_q2 - 1]
                    D2 = kr[a_q1 - 1, (1j @ 2 @ pi @ M @ np.arange(0, P - 1 + 1)).T * a_q2 - 1]
                    D = np.array([[D1, D2]])
                
                if Nr == 1:
                    CRB_mtx = get_crb_1d_UMA(A, D, Rx, noise_var, M)
                else:
                    CRB_mtx = get_crb_2d_UMA(A, D, Rx, noise_var, M)
                crb = diag[CRB_mtx - 1]
                bnd_dfo = np.linalg.lstsq(np.linalg.matrix_power(np.linalg.lstsq(0.5.T, M.T), 2).T, 3 .T)
                bnd_aoa = np.linalg.lstsq(1 .T, 3 .T)
                
                if Nr == 1:
                    crb_dfo = crb
                else:
                    crb_aoa = crb[np.arange(1, Q[i_Q - 1] + 1) - 1]
                    crb_dfo = crb[np.arange(Q[i_Q - 1] + 1, end + 1) - 1]
                crb_dfo(crb_dfo > bnd_dfo) = bnd_dfo
                crb_dfo(crb_dfo < -bnd_dfo) = -bnd_dfo
                
                if Nr > 1:
                    crb_aoa(crb_aoa > bnd_aoa) = bnd_aoa
                    crb_aoa(crb_aoa < -bnd_aoa) = -bnd_aoa
                
                if Nr == 1:
                    crb_aoa = 0
                    crb_dfo = mean[abs[crb_dfo - 1] - 1]
                else:
                    crb_aoa = mean[abs[crb_aoa - 1] - 1]
                    crb_dfo = mean[abs[crb_dfo - 1] - 1]
                r_dfo_crb_trial = r_dfo_crb_trial + crb_dfo
                r_aoa_crb_trial = r_aoa_crb_trial + crb_aoa
            r_dfo_crb(i_Q, i_snr) = np.linalg.lstsq(r_dfo_crb_trial.T, n_trial_q.T)
            r_aoa_crb(i_Q, i_snr) = np.linalg.lstsq(r_aoa_crb_trial.T, n_trial_q.T)
    return r_dfo_crb[r_aoa_crb]


def get_crb_2d_UMA(A, D, P, noise_var, snapshots):
    n = np.size(P, 1)
    m = np.size(A, 1)
    R = A @ P @ A.conj().T + noise_var @ eye[m - 1]
    H = D.conj().T @ (eye[m - 1] - np.linalg.lstsq(A.T, (A.conj().T @ A).T) @ A.conj().T) @ D
    U = np.linalg.lstsq((P @ A.conj().T).T, R.T) @ A @ P
    CRB_mtx = real[H * kron[np.ones((2,)) - 1, U - 1].T - 1]
    CRB_mtx = np.linalg.lstsq(np.linalg.lstsq(noise_var.T, 2 .T).T, snapshots.T) @ np.linalg.lstsq(eye[2 @ n - 1].T, CRB_mtx.T)
    return CRB_mtx


def get_crb_1d_UMA(A, D, P, noise_var, snapshots):
    n = np.size(P, 1)
    m = np.size(A, 1)
    R = A @ P @ A.conj().T + noise_var @ eye[m - 1]
    H = D.conj().T @ (eye[m - 1] - np.linalg.lstsq(A.T, (A.conj().T @ A).T) @ A.conj().T) @ D
    U = np.linalg.lstsq((P @ A.conj().T).T, R.T) @ A @ P
    CRB_mtx = real[H * U.T - 1]
    CRB_mtx = np.linalg.lstsq(np.linalg.lstsq(noise_var.T, 2 .T).T, snapshots.T) @ np.linalg.lstsq(eye[n - 1].T, CRB_mtx.T)
    return CRB_mtx


def get_src_mtx(x, eps_q, h_q, Q, M, N):
    X = np.zeros((Q, M))
    
    for i_Q in np.arange(1, Q + 1):
        h_q_vec = h_q[i_Q - 1, : - 1]
        yp = cconv[x.T - 1, h_q_vec - 1, N - 1]
        yp = yp[np.arange(1, M + 1) - 1]
        X(i_Q, :) = yp * exp[2j @ pi @ eps_q[i_Q - 1] @ np.arange(0, M - 1 + 1) - 1]
    return X