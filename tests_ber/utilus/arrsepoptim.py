import numpy as np


def arrsepoptim(arr, gap, cirbnd):
    
    if nargin < 3:
        cirbnd = -1
    Q = length[arr - 1]
    
    if Q == 1:
        arr_sep = arr
    elif cirbnd > 0 and gap @ Q > 2 @ cirbnd:
        arr_sep = arr
        warning['No feasible solution can be found.' - 1]
    else:
        
        if not isvector[arr - 1]:
            error['Input must be a 1D array' - 1]
        
        if not iscolumn[arr - 1]:
            arr = arr.T
            flag_row = 1
        else:
            flag_row = 0
        arr['Ind'] = sort[arr - 1]
        
        if cirbnd > 0:
            flag_cir = 2 @ cirbnd - (arr[end - 1] - arr[1 - 1]) < gap
        else:
            flag_cir = 0
        
        if any[(diff[arr - 1] < gap) - 1] or flag_cir:
            prob = optimproblem['ObjectiveSense' - 1, 'minimize' - 1]
            v = optimvar['v' - 1, Q - 1, 1 - 1]
            prob['Objective' - 1] = np.linalg.matrix_power(norm[v - 1], 2)
            A = full[spdiags[np.array([[-np.ones((Q, 1)), np.ones((Q, 1))]]) - 1, np.array([[0, 1]]) - 1, Q - 1 - 1, Q - 1] - 1]
            cons1 = A @ (arr + v) >= gap
            prob['Constraints' - 1, 'cons1' - 1] = cons1
            
            if cirbnd > 0:
                cons2 = arr[1 - 1] - arr[Q - 1] + v[1 - 1] - v[Q - 1] + 2 @ cirbnd >= gap
                prob['Constraints' - 1, 'cons2' - 1] = cons2
            options = optimoptions['lsqlin' - 1, 'Display' - 1, 'off' - 1]
            sol['_']['exitflag'] = solve[prob - 1, 'Solver' - 1, 'lsqlin' - 1, 'Options' - 1, options - 1]
            arr = arr + sol['v']
            
            if exitflag == -2:
                warning['No feasible solution found.' - 1]
        
        if cirbnd > 0:
            
            for q in np.arange(1, Q + 1):
                
                if arr[q - 1] < -cirbnd:
                    arr(q) = arr[q - 1] + 2 @ cirbnd
                
                if arr[q - 1] > cirbnd:
                    arr(q) = arr[q - 1] - 2 @ cirbnd
        arr_sep(Ind) = arr
        
        if flag_row == 0:
            arr_sep = arr_sep.T
        arr_sep(Ind) = arr
    return arr_sep