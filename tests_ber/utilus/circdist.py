import numpy as np


def circdist(arr1, arr2, circ_bnd, ignore_check):
    
    if nargin < 4:
        ignore_check = 0
    
    if ignore_check == 0:
        assert[(all[(abs[arr1 - 1] <= circ_bnd) - 1] and all[(abs[arr2 - 1] <= circ_bnd) - 1]) - 1, 'Array elements not in the range of [-cir_bnd, cir_bnd]' - 1]
    abs_dist = abs[arr1 - arr2 - 1]
    dist = min[abs_dist - 1, 2 @ circ_bnd - abs_dist - 1]
    return dist