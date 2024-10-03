import numpy as np


def parsave(savefile, varargin):
    name = cell[nargin - 1 - 1, 1 - 1]
    
    for ii in np.arange(1, nargin - 1 + 1):
        (name, ii)[] = inputname[ii + 1 - 1]
        eval[np.array([[(((name, ii),),), '=varargin{', str(ii), '};']]) - 1]
        (name, ii)[] = np.array([[",''", (((name, ii),),), "''"]])
    varnames = np.array([[(((name, :),),)]])
    comstring = np.array([["save(''", savefile, "''", varnames, ');']])
    eval[comstring - 1]