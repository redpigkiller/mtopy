import numpy as np


def baseN(num, base, num_digits):
    
    if nargin < 3:
        num_digits = ceil[np.linalg.lstsq(log[num + 1 - 1].T, log[base - 1].T) - 1]
    digits = np.zeros((1, num_digits))
    
    for idx in np.arange(num_digits, 1 + -1, -1):
        digits(idx) = mod[num - 1, base - 1]
        num = floor[np.linalg.lstsq(num.T, base.T) - 1]
    return digits