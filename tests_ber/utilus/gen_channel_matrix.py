import numpy as np


def gen_channel_matrix(dfo, aoa, chl, N, Q, Nr, SP, algo_flag, is_sparse):
    
    if algo_flag['assume_no_dfo'] == 1:
        dfo = np.zeros((Q, 1))
    
    if algo_flag['assume_no_aoa'] == 1:
        aoa = np.zeros((Q, 1))
    
    if nargin < 9:
        is_sparse = 1
    assert[(Q == length[dfo - 1]) - 1, 'unmatch number of paths' - 1]
    
    if Nr > 1:
        assert[(Q == length[aoa - 1]) - 1, 'unmatched Q' - 1]
    assert[(Q == np.size(chl, 1)) - 1, 'unmatched Q' - 1]
    
    if Nr == 1:
        A_hat = exp[-1j @ 2 @ pi @ SP @ np.zeros((1, Q, 'like', dfo)) - 1]
    else:
        A_hat = exp[-1j @ 2 @ pi @ SP @ aoa @ np.arange(0, Nr - 1 + 1) - 1].T
    
    if is_sparse == 0:
        B_hat = np.zeros((N @ Q, N, 'like', dfo))
        chl = np.array([[chl, np.zeros((Q, N - np.size(chl, 2), 'like', dfo))]])
        
        for i_Q in np.arange(1, Q + 1):
            DFO_q = diag[exp[1j @ 2 @ pi @ dfo[i_Q - 1] @ np.arange(0, N - 1 + 1) - 1] - 1]
            H_q = circulant(chl[i_Q - 1, : - 1].T, N)
            B_hat([(i_Q - 1) @ N + 1, i_Q @ N], :) = DFO_q @ H_q
    else:
        B_hat = cell[Q - 1, 1 - 1]
        
        for i_Q in np.arange(1, Q + 1):
            DFO_q = spdiags[exp[1j @ 2 @ pi @ dfo[i_Q - 1] @ np.arange(0, N - 1 + 1) - 1].T - 1, 0 - 1, N - 1, N - 1]
            chl_i['chl_j']['chl_v'] = find[chl[i_Q - 1, : - 1].T - 1]
            sph = sparse[chl_i - 1, chl_j - 1, chl_v - 1, N - 1, 1 - 1]
            H_q = circulant(sph, N)
            (B_hat, i_Q)[] = DFO_q @ H_q
        B_hat = vertcat[B_hat[: - 1] - 1]
    chl_mtx = kron[A_hat - 1, speye[N - 1] - 1] @ B_hat
    return chl_mtx