import numpy as np


def circulant(x, Lch):
    N = np.size(x, 1)
    Xcir = np.zeros((N, Lch, 'like', x))
    
    for i_Lch in np.arange(1, Lch + 1):
        Xcir(:, i_Lch) = circshift[x - 1, i_Lch - 1 - 1]
    return Xcir