import numpy as np


def arrcmp(sim_arr, exist_arr, del_zeros):
    
    if nargin < 3:
        del_zeros = 1
    n1 = length[sim_arr - 1]
    n2 = length[exist_arr - 1]
    indices = np.zeros((n1, 1))
    
    for ii in np.arange(1, n1 + 1):
        
        for jj in np.arange(1, n2 + 1):
            
            if sim_arr[ii - 1] == exist_arr[jj - 1]:
                indices(ii) = jj
                
                break
    
    if del_zeros != 0:
        indices(indices == 0) = None
    return indices