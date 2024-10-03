import numpy as np


def arrpairbruteforce(arr_ref, arr_hat, cirbnd):
    
    if not isvector[arr_ref - 1] or not isvector[arr_hat - 1]:
        error['Inputs must be a 1D array' - 1]
    
    if not iscolumn[arr_hat - 1]:
        arr_hat = arr_hat.T
        flag_row = 1
    else:
        flag_row = 0
    
    if nargin < 3:
        cirbnd = -1
    Q = length[arr_ref - 1]
    dist = np.zeros((Q, Q, 'like', arr_ref))
    
    if cirbnd > 0:
        
        for i_Q in np.arange(1, Q + 1):
            
            for ii_Q in np.arange(1, Q + 1):
                d = abs[arr_ref[i_Q - 1] - arr_hat[ii_Q - 1] - 1]
                dist(i_Q, ii_Q) = min[d - 1, 2 @ cirbnd - d - 1]
    else:
        
        for i_Q in np.arange(1, Q + 1):
            
            for ii_Q in np.arange(1, Q + 1):
                dist(i_Q, ii_Q) = abs[arr_ref[i_Q - 1] - arr_hat[ii_Q - 1] - 1]
    Ind = perms[np.arange(1, Q + 1) - 1]
    indices = np.size(Ind, 1)
    cost = inf
    min_idx = 0
    
    for p in np.arange(1, indices + 1):
        tot_cost = 0
        
        for q in np.arange(1, Q + 1):
            tot_cost = tot_cost + dist[q - 1, Ind[p - 1, q - 1] - 1]
        
        if tot_cost < cost:
            cost = tot_cost
            min_idx = p
    indices = Ind[min_idx - 1, : - 1].T
    arr_hat = arr_hat[indices - 1]
    
    if flag_row == 1:
        arr_hat = arr_hat.T
        indices = indices.T
    return arr_hat[indices][cost]