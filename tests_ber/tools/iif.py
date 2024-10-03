import numpy as np


def iif(cond, t, f):
    
    if cond:
        result = t
    else:
        result = f
    return result