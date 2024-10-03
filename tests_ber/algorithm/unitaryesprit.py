import numpy as np


def unitaryesprit(X, Q, args):
    P = np.size(X, 1)
    
    if Q > P:
        error['can NOT solve! since Q > P' - 1]
    
    if mod[P - 1, 2 - 1] == 0:
        QM = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye[np.linalg.lstsq(P.T, 2 .T) - 1, 'like' - 1, X - 1], 1j @ eye[np.linalg.lstsq(P.T, 2 .T) - 1, 'like' - 1, X - 1]], [flip, eye[np.linalg.lstsq(P.T, 2 .T) - 1, 'like' - 1, X - 1], -1j @ flip[eye[np.linalg.lstsq(P.T, 2 .T) - 1, 'like' - 1, X - 1] - 1]]])
        Qm = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye[np.linalg.lstsq(P.T, 2 .T) - 1 - 1, 'like' - 1, X - 1], np.zeros((np.linalg.lstsq(P.T, 2 .T) - 1, 1, 'like', X)), 1j @ eye[np.linalg.lstsq(P.T, 2 .T) - 1 - 1, 'like' - 1, X - 1]], [np.zeros((1, np.linalg.lstsq(P.T, 2 .T) - 1, 'like', X)), sqrt[2 - 1], np.zeros((1, np.linalg.lstsq(P.T, 2 .T) - 1, 'like', X))], [flip[eye[np.linalg.lstsq(P.T, 2 .T) - 1 - 1, 'like' - 1, X - 1] - 1], np.zeros((np.linalg.lstsq(P.T, 2 .T) - 1, 1, 'like', X)), -1j @ flip[eye[np.linalg.lstsq(P.T, 2 .T) - 1 - 1, 'like' - 1, X - 1] - 1]]])
    else:
        QM = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1], np.zeros((np.linalg.lstsq((P - 1).T, 2 .T), 1, 'like', X)), 1j @ eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1]], [np.zeros((1, np.linalg.lstsq((P - 1).T, 2 .T), 'like', X)), sqrt[2 - 1], np.zeros((1, np.linalg.lstsq((P - 1).T, 2 .T), 'like', X))], [flip[eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1] - 1], np.zeros((np.linalg.lstsq((P - 1).T, 2 .T), 1, 'like', X)), -1j @ flip[eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1] - 1]]])
        Qm = np.linalg.lstsq(1 .T, sqrt[2 - 1].T) @ np.array([[eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1], 1j @ eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1]], [flip, eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1], -1j @ flip[eye[np.linalg.lstsq((P - 1).T, 2 .T) - 1, 'like' - 1, X - 1] - 1]]])
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
    J2 = np.array([[np.zeros((P - 1, 1, 'like', X)), eye[P - 1 - 1, 'like' - 1, X - 1]]])
    Qm = Qm.conj().T @ J2 @ QM
    K1 = 2 @ real[Qm - 1] @ Es
    K2 = 2 @ imag[Qm - 1] @ Es
    
    if strcmpi[args['method'] - 1, 'LS' - 1]:
        R = np.linalg.lstsq(K1.conj().T @ K1, K1.conj().T) @ K2
    elif strcmpi[args['method'] - 1, 'TLS' - 1]:
        _['_']['U'] = svd[np.array([[K1, K2]]) - 1]
        U12 = U[np.arange(1, Q + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        U22 = U[np.arange(Q + 1, end + 1) - 1, np.arange(Q + 1, end + 1) - 1]
        R = np.linalg.lstsq((-U12).T, U22.T)
    else:
        error['wrong method' - 1]
    w = eig[R - 1]
    
    if any[(imag[w - 1] != 0) - 1]:
        r_test = 0
    else:
        r_test = 1
    w = real[w - 1]
    f = np.linalg.lstsq(atan[w - 1].T, pi.T)
    return f[r_test]