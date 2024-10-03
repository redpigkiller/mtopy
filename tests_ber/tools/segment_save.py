import numpy as np


def segment_save(inpt_data, seg_size):
    Mc = np.size(inpt_data, np.ndim(inpt_data))
    otherdims = repmat[[[':']] - 1, 1 - 1, np.ndim(inpt_data) - 1 - 1]
    
    if Mc < seg_size:
        n_seg = 1
    else:
        n_seg = ceil[np.linalg.lstsq(Mc.T, seg_size.T) - 1]
    oupt_data = cell[n_seg - 1, 1 - 1]
    
    for i_seg in np.arange(1, n_seg + 1):
        
        if i_seg @ seg_size <= Mc:
            (oupt_data, i_seg)[] = inpt_data[otherdims[: - 1] - 1, np.arange((i_seg - 1) @ seg_size + 1, i_seg @ seg_size + 1) - 1]
        else:
            (oupt_data, i_seg)[] = inpt_data[otherdims[: - 1] - 1, np.arange((i_seg - 1) @ seg_size + 1, Mc + 1) - 1]
    return oupt_data