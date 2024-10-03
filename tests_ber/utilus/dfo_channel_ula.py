import numpy as np


def dfo_channel_ula(x, n, eps_q, theta_q, h_q, N, Q, Nr, SP, flag_noise, add_CP_len):
    
    if nargin < 7:
        add_CP_len = 0
    assert[(N == length[x - 1]) - 1, 'unmatch OFDM block size' - 1]
    assert[(Q == length[eps_q - 1]) - 1, 'unmatch number of paths' - 1]
    assert[(Q == length[theta_q - 1] and Q == np.size(h_q, 1)) - 1, 'unmatched Q' - 1]
    assert[(Nr == np.linalg.lstsq(length[n - 1].T, N.T)) - 1, 'unmatch number of RX antennas' - 1]
    Y = np.zeros((N, Nr, 'like', x))
    
    if add_CP_len > 0:
        x = np.array([[x[[end - add_CP_len + 1, end] - 1]], [x]])
        
        for m in np.arange(1, Nr + 1):
            
            for i_Q in np.arange(1, Q + 1):
                h_q_vec = h_q[i_Q - 1, : - 1]
                yp = conv[x.T - 1, h_q_vec - 1]
                yp = yp * exp[1j @ 2 @ pi @ eps_q[i_Q - 1] @ np.arange(-add_CP_len, length[yp - 1] - add_CP_len - 1 + 1) - 1]
                yp = yp @ exp[-1j @ 2 @ pi @ SP @ theta_q[i_Q - 1] @ (m - 1) - 1]
                Y(:, m) = Y[: - 1, m - 1] + yp[np.arange(add_CP_len + 1, add_CP_len + N + 1) - 1].T
    else:
        
        for m in np.arange(1, Nr + 1):
            
            for i_Q in np.arange(1, Q + 1):
                h_q_vec = h_q[i_Q - 1, : - 1]
                yp = cconv[x.T - 1, h_q_vec - 1, N - 1]
                yp = yp * exp[1j @ 2 @ pi @ eps_q[i_Q - 1] @ np.arange(0, N - 1 + 1) - 1]
                yp = yp @ exp[-1j @ 2 @ pi @ SP @ theta_q[i_Q - 1] @ (m - 1) - 1]
                Y(:, m) = Y[: - 1, m - 1] + yp.T
    
    if flag_noise:
        y = Y[: - 1] + n
    else:
        y = Y[: - 1]
    return y