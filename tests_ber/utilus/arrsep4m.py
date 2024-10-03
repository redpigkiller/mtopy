import numpy as np


def arrsep4m(arr, gap, cirbnd, tol):
    
    if nargin < 3:
        cirbnd = -1
    
    if nargin < 4:
        tol = 1e-15
    assert[isvector[arr - 1] - 1, 'Input must be a 1D array' - 1]
    flag_row = not iscolumn[arr - 1]
    N = length[arr - 1]
    
    if N == 1:
        new_arr = arr
        
        return
    elif cirbnd > 0 and gap @ N > 2 @ cirbnd:
        new_arr = arr
        warning['No feasible solution can be found.' - 1]
        
        return
    new_arr = np.array([[arr[1 - 1]]])
    sort_arr = np.array([[arr[1 - 1]]])
    
    for n in np.arange(2, N + 1):
        new_arr = insert_sort(new_arr, arr[n - 1])
        sort_arr = insert_sort(sort_arr, arr[n - 1])
        d_arr = diff[new_arr - 1]
        Ind = find[(d_arr < gap) - 1]
        
        if cirbnd > 0:
            flag_cir = 2 @ cirbnd - (new_arr[n - 1] - new_arr[1 - 1]) < gap
        else:
            flag_cir = 0
        
        while not isempty[Ind - 1] or flag_cir:
            
            if not isempty[Ind - 1]:
                Ind = Ind[1 - 1]
                d0 = gap - d_arr[Ind - 1]
                count_l = 1
                
                for idx in np.arange(Ind - 1, 1 + -1, -1):
                    
                    if d_arr[idx - 1] - gap < tol:
                        count_l = count_l + 1
                    else:
                        
                        break
                count_r = 1
                
                for idx in np.arange(Ind + 1, n - 1 + 1):
                    
                    if d_arr[idx - 1] - gap < tol:
                        count_r = count_r + 1
                    else:
                        
                        break
                push_l = np.linalg.lstsq((d0 @ count_r).T, (count_r + count_l).T)
                push_r = np.linalg.lstsq((d0 @ count_l).T, (count_r + count_l).T)
                
                if push_l < eps[new_arr[Ind - 1] - 1]:
                    push_l = eps[new_arr[Ind - 1] - 1]
                
                if push_r < eps[new_arr[Ind - 1] - 1]:
                    push_r = eps[new_arr[Ind - 1] - 1]
                
                for c in np.arange(1, count_l + 1):
                    new_arr(Ind + 1 - c) = new_arr[Ind + 1 - c - 1] - push_l
                
                for c in np.arange(1, count_r + 1):
                    new_arr(Ind + c) = new_arr[Ind + c - 1] + push_r
            else:
                d1 = gap - (2 @ cirbnd - (new_arr[n - 1] - new_arr[1 - 1]))
                count_l = 1
                
                for idx in np.arange(n - 1, 1 + -1, -1):
                    
                    if d_arr[idx - 1] - gap < tol:
                        count_l = count_l + 1
                    else:
                        
                        break
                count_r = 1
                
                for idx in np.arange(1, n - 1 + 1):
                    
                    if d_arr[idx - 1] - gap < tol:
                        count_r = count_r + 1
                    else:
                        
                        break
                push_l = np.linalg.lstsq((d1 @ count_r).T, (count_r + count_l).T)
                push_r = np.linalg.lstsq((d1 @ count_l).T, (count_r + count_l).T)
                
                if push_l < eps[new_arr[Ind - 1] - 1]:
                    push_l = eps[new_arr[Ind - 1] - 1]
                
                if push_r < eps[new_arr[Ind - 1] - 1]:
                    push_r = eps[new_arr[Ind - 1] - 1]
                
                for c in np.arange(1, count_l + 1):
                    new_arr(n + 1 - c) = new_arr[n + 1 - c - 1] - push_l
                
                for c in np.arange(1, count_r + 1):
                    new_arr(c) = new_arr[c - 1] + push_r
            d_arr = diff[new_arr - 1]
            Ind = find[(d_arr < gap) - 1]
            
            if cirbnd > 0:
                flag_cir = 2 @ cirbnd - (new_arr[n - 1] - new_arr[1 - 1]) < gap
            else:
                flag_cir = 0
    
    if cirbnd > 0:
        
        for n in np.arange(1, N + 1):
            
            if new_arr[n - 1] < -cirbnd:
                new_arr(n) = new_arr[n - 1] + 2 @ cirbnd
            
            if new_arr[n - 1] > cirbnd:
                new_arr(n) = new_arr[n - 1] - 2 @ cirbnd
    Ind = arrcmp(arr, sort_arr)
    new_arr = new_arr[Ind - 1]
    
    if flag_row:
        new_arr = new_arr.T
    return new_arr


def insert_sort(x, val):
    N = length[x - 1]
    
    if N == 0:
        y = val
        
        return
    idx = 1
    
    while idx <= N:
        
        if val < x[idx - 1]:
            
            break
        idx = idx + 1
    
    if idx == 1:
        y = np.array([[val], [x]])
    elif idx == N + 1:
        y = np.array([[x], [val]])
    else:
        y = np.array([[x[[1, idx - 1] - 1]], [val], [x[[idx, end] - 1]]])
    return y