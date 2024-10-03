import numpy as np


def unitaryesprit_2d(X, Mx, Q, args):
    M = np.size(X, 1)
    assert[(mod[M - 1, Mx - 1] == 0) - 1, 'invalid array manifold!' - 1]
    My = np.linalg.lstsq(M.T, Mx.T)
    QM = pi_real(M)
    T = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ QM.conj().T @ np.array([[X + flip[conj[X - 1] - 1, 1 - 1], 1j @ (X - flip[conj[X - 1] - 1, 1 - 1])]])
    T = real[T - 1]
    
    if strcmpi[args['sig_subspace'] - 1, 'SVD' - 1]:
        Es['_'] = svd[T - 1]
    elif strcmpi[args['sig_subspace'] - 1, 'EVD' - 1]:
        Es['eigvar'] = eig[T @ T.conj().T - 1]
        eigvar = diag[eigvar - 1]
        _['ind'] = sort[eigvar - 1, 'descend' - 1]
        Es = Es[: - 1, ind - 1]
    else:
        error['wrong sig_subspace' - 1]
    Es = Es[: - 1, np.arange(1, Q + 1) - 1]
    Qmx = pi_real((Mx - 1) @ My)
    Qmy = pi_real(Mx @ (My - 1))
    Ju2 = np.array([[np.zeros((Mx - 1, 1, 'like', X)), eye[Mx - 1 - 1, 'like' - 1, X - 1]]])
    Jv2 = np.array([[np.zeros((My - 1, 1, 'like', X)), eye[My - 1 - 1, 'like' - 1, X - 1]]])
    Ju2 = kron[eye[My - 1, 'like' - 1, X - 1] - 1, Ju2 - 1]
    Jv2 = kron[Jv2 - 1, eye[Mx - 1, 'like' - 1, X - 1] - 1]
    Qmx = Qmx.conj().T @ Ju2 @ QM
    Qmy = Qmy.conj().T @ Jv2 @ QM
    Ku1 = 2 @ real[Qmx - 1] @ Es
    Ku2 = 2 @ imag[Qmx - 1] @ Es
    Kv1 = 2 @ real[Qmy - 1] @ Es
    Kv2 = 2 @ imag[Qmy - 1] @ Es
    
    if strcmpi[args['method'] - 1, 'LS' - 1]:
        Ru = np.linalg.lstsq(Ku1.conj().T @ Ku1, Ku1.conj().T) @ Ku2
        Rv = np.linalg.lstsq(Kv1.conj().T @ Kv1, Kv1.conj().T) @ Kv2
    elif strcmpi[args['method'] - 1, 'TLS' - 1]:
        _['_']['U'] = svd[np.array([[Ku1, Ku2]]) - 1]
        U12 = U[np.arange(1, Q + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        U22 = U[np.arange(Q + 1, end + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        Ru = np.linalg.lstsq((-U12).T, U22.T)
        _['_']['U'] = svd[np.array([[Kv1, Kv2]]) - 1]
        U12 = U[np.arange(1, Q + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        U22 = U[np.arange(Q + 1, end + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        Rv = np.linalg.lstsq((-U12).T, U22.T)
    else:
        error['wrong method' - 1]
    w = eig[Ru + 1j @ Rv - 1]
    fu = np.linalg.lstsq(atan[real[w - 1] - 1].T, pi.T)
    fv = np.linalg.lstsq(atan[imag[w - 1] - 1].T, pi.T)
    return fu[fv]


def pi_real(m):
    
    if mod[m - 1, 2 - 1] == 0:
        Qm = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye, np.linalg.lstsq(m.T, 2 .T), 1j @ eye[np.linalg.lstsq(m.T, 2 .T) - 1]], [flip, eye[np.linalg.lstsq(m.T, 2 .T) - 1], -1j @ flip[eye[np.linalg.lstsq(m.T, 2 .T) - 1] - 1]]])
    else:
        Qm = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye[np.linalg.lstsq((m - 1).T, 2 .T) - 1], np.zeros((np.linalg.lstsq((m - 1).T, 2 .T), 1)), 1j @ eye[np.linalg.lstsq((m - 1).T, 2 .T) - 1]], [np.zeros((1, np.linalg.lstsq((m - 1).T, 2 .T))), sqrt[2 - 1], np.zeros((1, np.linalg.lstsq((m - 1).T, 2 .T)))], [flip[eye[np.linalg.lstsq((m - 1).T, 2 .T) - 1] - 1], np.zeros((np.linalg.lstsq((m - 1).T, 2 .T), 1)), -1j @ flip[eye[np.linalg.lstsq((m - 1).T, 2 .T) - 1] - 1]]])
    return Qm