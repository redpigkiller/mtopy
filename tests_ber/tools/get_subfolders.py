import numpy as np


def get_subfolders(directory):
    d = dir[directory - 1]
    d = d[np.array([[(d[: - 1], 'isdir')]]) - 1]
    d = d[(not ismember[[[(d[: - 1], 'name')]] - 1, [['.', '..']] - 1]) - 1]
    subfolders = [[(d[: - 1], 'name')]]
    n_subfolders = length[d - 1]
    _['Ind'] = sort[np.array([[(d[: - 1], 'datenum')]]) - 1, 'descend' - 1]
    
    if not isempty[Ind - 1]:
        sorted_idx = Ind
    else:
        sorted_idx = 0
    return subfolders[n_subfolders][sorted_idx]