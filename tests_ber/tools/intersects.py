import numpy as np


def intersects(src, varargin):
    unmatched = 0
    
    if nargin <= 1:
        tgt = src
    else:
        
        if length[src - 1] != length[varargin[1 - 1] - 1]:
            unmatched = 1
        tgt = intersect[src - 1, varargin[1 - 1] - 1]
        
        for ii in np.arange(2, nargin - 1 + 1):
            
            if length[tgt - 1] != length[varargin[ii - 1] - 1]:
                unmatched = 1
            tgt = intersect[tgt - 1, varargin[ii - 1] - 1]
    return tgt[unmatched]