import numpy as np


def nan2zero(arr, val):
    
    if nargin < 2:
        val = 0
    arr(isnan[arr - 1]) = val
    return arr