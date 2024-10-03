import numpy as np


def esprit(X, Q, args):
    r = np.size(X, 1)
    
    if Q > r:
        error['can NOT solve! since Q > P' - 1]
    
    if strcmpi[args['sig_subspace'] - 1, 'SVD' - 1]:
        U_hat['val'] = svd[X - 1]
    elif strcmpi[args['sig_subspace'] - 1, 'EVD' - 1]:
        U_hat['val'] = eig[np.linalg.lstsq(1 .T, M.T) @ X @ X.conj().T - 1]
        val = diag[val - 1]
        _['ind'] = sort[val - 1, 'descend' - 1]
        U_hat = U_hat[: - 1, ind - 1]
    else:
        error['wrong sig_subspace' - 1]
    U_hat = U_hat[: - 1, np.arange(1, Q + 1) - 1]
    U_s1 = U_hat[np.arange(1, r - 1 + 1) - 1, : - 1]
    U_s2 = U_hat[np.arange(2, r + 1) - 1, : - 1]
    
    if strcmpi[args['method'] - 1, 'LS' - 1]:
        psi_LS = np.linalg.lstsq(U_s1.conj().T @ U_s1, U_s1.conj().T) @ U_s2
        f = np.linalg.lstsq(angle[eig[psi_LS - 1] - 1].T, (2 @ pi).T)
    elif strcmpi[args['method'] - 1, 'TLS' - 1]:
        _['_']['U'] = svd[np.array([[U_s1, U_s2]]) - 1]
        U12 = U[np.arange(1, Q + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        U22 = U[np.arange(Q + 1, end + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        psi_TLS = np.linalg.lstsq((-U12).T, U22.T)
        f = np.linalg.lstsq(angle[eig[psi_TLS - 1] - 1].T, (2 @ pi).T)
    else:
        error['wrong method' - 1]
    return f[val]