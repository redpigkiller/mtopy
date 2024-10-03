import numpy as np


def segment_load(load_Mc_idx, seg_size):
    load_idx = floor[np.linalg.lstsq((load_Mc_idx - 1).T, seg_size.T) - 1] + 1
    sub_idx = mod[load_Mc_idx - 1 - 1, seg_size - 1] + 1
    return load_idx[sub_idx]