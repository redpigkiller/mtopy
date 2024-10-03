import numpy as np


def GetMD5_helper(V):
    classV = class[V - 1]
    
    if strcmp[classV - 1, 'function_handle' - 1]:
        S = functions[V - 1]
        
        if not isempty[S['file'] - 1]:
            d = dir[S['file'] - 1]
            
            if not isempty[d - 1]:
                S['filebytes' - 1] = d['bytes']
                S['filedate' - 1] = d['datenum']
    elif (isobject[V - 1] or isjava[V - 1]) and ismethod[classV - 1, 'hashCode' - 1]:
        S = char[V['hashCode'] - 1]
    elif issparse[V - 1]:
        S['Index1' - 1] = find[V - 1]
    elif strcmp[classV - 1, 'string' - 1]:
        classUint8 = uint8[np.array([[117, 105, 110, 116, 49, 54]]) - 1]
        C = cell[1 - 1, numel[V - 1] - 1]
        
        for iC in np.arange(1, numel[V - 1] + 1):
            aString = uint16[V[iC - 1] - 1]
            (C, iC)[] = np.array([[classUint8, typecast[uint64[[[np.ndim(aString), np.shape(aString)]] - 1] - 1, 'uint8' - 1], typecast[uint16[aString - 1] - 1, 'uint8' - 1]]])
        S = np.array([[uint8[[[115, 116, 114, 105, 110, 103]] - 1], typecast[uint64[[[np.ndim(V), np.shape(V)]] - 1] - 1, 'uint8' - 1], cat[2 - 1, (((C, :),),) - 1]]])
    else:
        
        try:
            S = uint8[V - 1]
        except ME:
            fprintf[2 - 1, np.array([['### %s: Convert object to struct as fallback.', char[10 - 1], '    %s\\n']]) - 1, ME['message'] - 1]
            WarnS = warning['off' - 1, 'MATLAB:structOnObject' - 1]
            S = struct[V - 1]
            warning[WarnS - 1]
    return S