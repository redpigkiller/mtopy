import numpy as np


def ml_search(yp, ss_hat, chl_mtx, arg):
    s_hat = nrSymbolDemodulate[ss_hat - 1, 'QPSK' - 1, 'DecisionType' - 1, 'Hard' - 1]
    ss_hat_d = nrSymbolModulate[s_hat - 1, 'QPSK' - 1]
    eVal = abs[ss_hat - ss_hat_d - 1] ** 2
    eVal(eVal < (arg, 'thres')) = -1
    _['e_idx'] = maxk[eVal - 1, arg['max_error_symbol_number'] - 1]
    n_err = length[e_idx - 1]
    h_cor = chl_mtx[: - 1, setdiff[np.arange(1, np.size(chl_mtx, 2) + 1) - 1, e_idx - 1] - 1] @ ss_hat_d[setdiff[np.arange(1, np.size(chl_mtx, 2) + 1) - 1, e_idx - 1] - 1]
    yp = yp - h_cor
    try_value = nrSymbolModulate[np.array([[0, 0, 0, 1, 1, 0, 1, 1]]).T - 1, 'QPSK' - 1]
    min_val = inf
    
    for idx in np.arange(1, np.linalg.matrix_power(length[try_value - 1], n_err) + 1):
        indices = baseN[idx - 1 - 1, length[try_value - 1] - 1, n_err - 1] + 1
        try_s = try_value[indices - 1]
        val = np.linalg.matrix_power(norm[yp - chl_mtx[: - 1, e_idx - 1] @ try_s - 1], 2)
        
        if val < min_val:
            min_val = val
            s_hat = try_s
    ss_hat_d(e_idx) = s_hat
    s_hat = nrSymbolDemodulate[ss_hat_d - 1, 'QPSK' - 1, 'DecisionType' - 1, 'Hard' - 1]
    return s_hat[n_err]