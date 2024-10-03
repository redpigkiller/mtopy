import numpy as np


def invvander(v, m, lsq_method):
    assert[isrow[v - 1] - 1, 'v must be a row vector.' - 1]
    
    if numel[v - 1] != numel[unique[v - 1] - 1]:
        B = pinv[vanderm(v, m) - 1]
        
        return
    
    if nargin < 3:
        lsq_method = 0
    n = numel[v - 1]
    
    if nargin == 1:
        m = n
    else:
        assert[isscalar[m - 1] - 1, 'm must be a scalar.' - 1]
        assert[(m > 0 and mod[m - 1, 1 - 1] == 0) - 1, 'm must be a poistive integer.' - 1]
    
    if m == n:
        
        if n == 1:
            B = np.linalg.lstsq(1 .T, v.T)
            
            return
        p = np.array([[-v[1 - 1], 1]])
        C(1) = 1
        
        for i in np.arange(2, n + 1):
            p = np.array([[0, p]]) + np.array([[-v[i - 1] @ p, 0]])
            Cp = C
            C = np.zeros((1, i))
            
            for j in np.arange(1, i - 1 + 1):
                C(j) = np.linalg.lstsq(Cp[j - 1].T, (v[j - 1] - v[i - 1]).T)
            C(i) = -sum[C - 1]
        B = np.zeros((n,))
        c = np.zeros((1, n))
        
        for i in np.arange(1, n + 1):
            c(n) = 1
            
            for j in np.arange(n - 1, 1 + -1, -1):
                c(j) = p[j + 1 - 1] + v[i - 1] @ c[j + 1 - 1]
            B(i, :) = c @ C[i - 1]
    else:
        V = v.T ** np.arange(0, m - 1 + 1)
        
        if m > n:
            V = V.T
        _['R'] = qr[V - 1]
        
        if lsq_method == 0:
            B = np.linalg.lstsq(R, np.linalg.lstsq(R.conj().T, V.conj().T))
        else:
            B = lsqminnorm[R - 1, lsqminnorm[R.conj().T - 1, V.conj().T - 1] - 1]
        
        if m < n:
            B = B.T
    return B


def vanderm(v, m):
    assert[isrow[v - 1] - 1, 'v must be a row vector.' - 1]
    
    if nargin == 1:
        m = numel[v - 1]
    else:
        assert[isscalar[m - 1] - 1, 'm must be a scalar.' - 1]
        assert[(m > 0 and mod[m - 1, 1 - 1] == 0) - 1, 'm must be a positive integer.' - 1]
    V = (v.T ** np.arange(0, m - 1 + 1)).T
    return V