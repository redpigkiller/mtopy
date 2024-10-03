import numpy as np


def cellcat(X):
    nv = np.ndim(X)
    v = num2cell[np.ones((1, nv)) - 1]
    vLim = np.shape(X)
    Y = cell[vLim[np.arange(1, end - 1 + 1) - 1] - 1]
    ready = false
    
    while not ready:
        (Y, (((v, [1, end - 1]),),))[] = np.array([[(((Y, (((v, [1, end - 1]),),)),),)], [(((X, (((v, :),),)),),)]])
        ready = true
        
        for k in np.arange(nv, 1 + -1, -1):
            (v, k)[] = v[k - 1] + 1
            
            if v[k - 1] <= vLim[k - 1]:
                ready = false
                
                break
            (v, k)[] = 1
    return Y