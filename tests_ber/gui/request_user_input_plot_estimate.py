import numpy as np


def request_user_input_plot_estimate():
    dir_res_now = get_subfolders_r['results' - 1, 2 - 1]
    
    if dir_res_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation result.\\n' - 1]
        
        return
    dir_now = struct
    count = 0
    name = [[]]
    array = None
    
    for i_arr in np.arange(1, (dir_res_now, 'count') + 1):
        exp_struct = dir_res_now['array'][i_arr - 1]
        
        if exp_struct['count'] != 0:
            res_exp_struct = struct
            count1 = 0
            name1 = [[]]
            array1 = None
            
            for ii_arr in np.arange(1, (exp_struct, 'count') + 1):
                subdir = fullfile['results' - 1, (dir_res_now, 'name')[i_arr - 1] - 1, (exp_struct, 'name')[ii_arr - 1] - 1]
                subdir = fullfile[subdir - 1, '*.est.mat' - 1]
                res_files = dir[subdir - 1]
                
                if not isempty[res_files - 1]:
                    count1 = count1 + 1
                    (name1, end + 1)[] = (exp_struct, 'name')[ii_arr - 1]
                    array1 = np.array([[array1], [(exp_struct, 'array')[ii_arr - 1]]])
            res_exp_struct['count' - 1] = count1
            res_exp_struct['name' - 1] = name1
            res_exp_struct['array' - 1] = array1
            
            if count1 != 0:
                count = count + 1
                (name, end + 1)[] = (dir_res_now, 'name')[i_arr - 1]
                array = np.array([[array], [res_exp_struct]])
    dir_now['count' - 1] = count
    dir_now['name' - 1] = name
    dir_now['array' - 1] = array
    defAns = struct
    sim_ind = 1
    defAns['sim_name' - 1] = dir_now['name'][sim_ind - 1]
    defAns['exp_name' - 1] = (dir_now, 'array')[sim_ind - 1]['name'][1 - 1]
    md5 = GetMD5[dir_now - 1, 'Array' - 1]
    defVal_path = fullfile['_tmp' - 1, 'defaultInput_plot_estimate.mat' - 1]
    
    if isfile[defVal_path - 1]:
        defVal = load[defVal_path - 1]['defVal']
        md5_prev = defVal['md5']
        
        if strcmp[md5 - 1, md5_prev - 1]:
            sim_ind = defVal['sim_ind']
            defAns = defVal['defAns']
        else:
            sim_ind = 1
            defAns['sim_name' - 1] = dir_now['name'][sim_ind - 1]
            defAns['exp_name' - 1] = (dir_now, 'array')[sim_ind - 1]['name'][1 - 1]
    prompt = [[]]
    title = 'Plot setting'
    formats = [[]]
    options = struct
    prompt(1, :) = [['Enter simulation data name:', 'sim_name', [[]]]]
    formats[1 - 1, 1 - 1]['type' - 1] = 'list'
    formats[1 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[1 - 1, 1 - 1]['size' - 1] = -1
    formats[1 - 1, 1 - 1]['format' - 1] = 'text'
    formats[1 - 1, 1 - 1]['items' - 1] = dir_now['name']
    formats[1 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    prompt(2, :) = [['experiment', 'exp_name', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'list'
    formats[2 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[2 - 1, 1 - 1]['size' - 1] = -1
    formats[2 - 1, 1 - 1]['format' - 1] = 'text'
    formats[2 - 1, 1 - 1]['items' - 1] = (dir_now, 'array')[sim_ind - 1]['name']
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    
    if IsCancelled == 0:
        answer['sim_name' - 1] = (answer, 'sim_name')[1 - 1]
        answer['exp_name' - 1] = (answer, 'exp_name')[1 - 1]
        defVal = struct
        defVal['md5' - 1] = md5
        sim_ind = find[ismember[dir_now['name'] - 1, answer['sim_name'] - 1] - 1]
        defVal['sim_ind' - 1] = sim_ind
        defVal['defAns' - 1] = answer
        
        if not exist['_tmp' - 1, 'dir' - 1]:
            mkdir['_tmp' - 1]
        save[defVal_path - 1, 'defVal' - 1]
    return answer[IsCancelled]