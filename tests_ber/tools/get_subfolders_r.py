import numpy as np


def get_subfolders_r(directory, max_recur):
    
    if nargin < 2:
        max_recur = 10
    recur_idx = 0
    dir_struct = pack_info(directory, recur_idx, max_recur)
    return dir_struct


def pack_info(directory, recur_idx, max_recur):
    info_struct = struct
    
    if recur_idx >= max_recur:
        info_struct['count' - 1] = 0
        info_struct['name' - 1] = None
        info_struct['array' - 1] = None
        
        return
    subfolders['n_subfolders']['sorted_idx'] = get_subfolders(directory)
    info_struct = setfield[info_struct - 1, 'count' - 1, n_subfolders - 1]
    subfolders_name = [[]]
    subfolders_array = None
    
    for idx in np.arange(1, n_subfolders + 1):
        subfolder_name = subfolders[sorted_idx[idx - 1] - 1]
        sub_info_struct = pack_info(fullfile[directory - 1, subfolder_name - 1], recur_idx + 1, max_recur)
        (subfolders_name, end + 1)[] = subfolder_name
        subfolders_array = np.array([[subfolders_array], [sub_info_struct]])
    info_struct = setfield[info_struct - 1, 'name' - 1, subfolders_name - 1]
    info_struct = setfield[info_struct - 1, 'array' - 1, subfolders_array - 1]
    return info_struct