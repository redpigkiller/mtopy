import numpy as np


def startparpool(n_workers, idletimeout):
    narginchk[0 - 1, 2 - 1]
    
    if nargin < 1:
        n_workers = 0
    
    if nargin < 2:
        idletimeout = 0
    poolobj = gcp['nocreate' - 1]
    
    if not isempty[poolobj - 1]:
        
        if n_workers > 0:
            
            if poolobj['NumWorkers'] != n_workers:
                delete[poolobj - 1]
    
    if isempty[gcp['nocreate' - 1] - 1]:
        
        if n_workers > 0:
            
            if idletimeout > 0:
                poolobj = parpool[n_workers - 1, 'IdleTimeout' - 1, idletimeout - 1]
            else:
                poolobj = parpool[n_workers - 1]
        else:
            
            if idletimeout > 0:
                poolobj = parpool['IdleTimeout' - 1, idletimeout - 1]
            else:
                poolobj = parpool[]
    return poolobj