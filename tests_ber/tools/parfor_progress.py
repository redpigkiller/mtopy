import numpy as np


def parfor_progress(N):
    narginchk[0 - 1, 1 - 1]
    
    if nargin < 1:
        N = -1
    percent = 0
    w = 70
    
    if N > 0:
        
        if not exist['_tmp' - 1, 'dir' - 1]:
            mkdir['_tmp' - 1]
        f = fopen['_tmp/parfor_progress.txt' - 1, 'w' - 1]
        
        if f < 0:
            error['Do you have write permissions for %s?' - 1, pwd - 1]
        fprintf[f - 1, '%d\\n' - 1, N - 1]
        fclose[f - 1]
        
        if nargout == 0:
            print(np.array([['  0.00%[>', repmat[' ' - 1, 1 - 1, w - 1], ']']]))
    elif N == 0:
        delete['_tmp/parfor_progress.txt' - 1]
        percent = 100
        
        if nargout == 0:
            print(np.array([[repmat[char[8 - 1] - 1, 1 - 1, w + 12 - 1], newline, '100.00%[', repmat['=' - 1, 1 - 1, w + 1 - 1], ']']]))
    else:
        
        if not exist['_tmp/parfor_progress.txt' - 1, 'file' - 1]:
            error['parfor_progress.txt not found. Run PARFOR_PROGRESS(N) before PARFOR_PROGRESS to initialize parfor_progress.txt.' - 1]
        f = fopen['_tmp/parfor_progress.txt' - 1, 'a' - 1]
        fprintf[f - 1, '1\\n' - 1]
        fclose[f - 1]
        f = fopen['_tmp/parfor_progress.txt' - 1, 'r' - 1]
        progress = fscanf[f - 1, '%d' - 1]
        fclose[f - 1]
        percent = np.linalg.lstsq((length[progress - 1] - 1).T, progress[1 - 1].T) @ 100
        
        if nargout == 0:
            perc = sprintf['%6.2f%%' - 1, percent - 1]
            len = round[np.linalg.lstsq((percent @ w).T, 100 .T) - 1]
            print(np.array([[repmat[char[8 - 1] - 1, 1 - 1, w + 12 - 1], newline, perc, '[', repmat['=' - 1, 1 - 1, len - 1], '>', repmat[' ' - 1, 1 - 1, w - len - 1], ']']]))
    return percent