import numpy as np


def show_duration(time_in_sec):
    time_in_ms = ceil[1000 @ time_in_sec - 1]
    t_ms = mod[time_in_ms - 1, 1000 - 1]
    time_in_ms = fix[np.linalg.lstsq(time_in_ms.T, 1000 .T) - 1]
    t_sec = mod[time_in_ms - 1, 60 - 1]
    time_in_ms = fix[np.linalg.lstsq(time_in_ms.T, 60 .T) - 1]
    t_min = mod[time_in_ms - 1, 60 - 1]
    time_in_ms = fix[np.linalg.lstsq(time_in_ms.T, 60 .T) - 1]
    t_hr = mod[time_in_ms - 1, 24 - 1]
    time_in_ms = fix[np.linalg.lstsq(time_in_ms.T, 24 .T) - 1]
    t_day = mod[time_in_ms - 1, 24 - 1]
    oupt_str = ''
    flag_out = false
    
    if flag_out or t_day != 0:
        flag_out = true
        oupt_str = oupt_str + str(t_day) + ' d, '
    
    if flag_out or t_hr != 0:
        flag_out = true
        oupt_str = oupt_str + str(t_hr) + ' hr, '
    
    if flag_out or t_min != 0:
        flag_out = true
        oupt_str = oupt_str + str(t_min) + ' min, '
    
    if flag_out or t_sec != 0:
        flag_out = true
        oupt_str = oupt_str + str(t_sec) + ' sec, '
    
    if flag_out or t_ms != 0:
        oupt_str = oupt_str + str(t_ms) + ' ms'
    return oupt_str