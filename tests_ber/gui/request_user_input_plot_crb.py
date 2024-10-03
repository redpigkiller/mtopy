import numpy as np


def request_user_input_plot_crb():
    dir_res_now_est = get_subfolders_r['results' - 1, 2 - 1]
    
    if dir_res_now_est['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation result.\\n' - 1]
        
        return
    dir_res_now_crb = get_subfolders_r['results_crb' - 1, 2 - 1]
    
    if dir_res_now_crb['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation result.\\n' - 1]
        
        return
    dir_now_crb = struct
    dir_now_est = struct
    count_crb = 0
    name_crb = [[]]
    array_crb = None
    count_est = 0
    name_est = [[]]
    array_est = None
    
    for i_arr in np.arange(1, (dir_res_now_crb, 'count') + 1):
        exp_struct = dir_res_now_crb['array'][i_arr - 1]
        
        if exp_struct['count'] != 0:
            res_exp_struct = struct
            count1 = 0
            name1 = [[]]
            array1 = None
            
            for ii_arr in np.arange(1, (exp_struct, 'count') + 1):
                subdir = fullfile['results_crb' - 1, (dir_res_now_crb, 'name')[i_arr - 1] - 1, (exp_struct, 'name')[ii_arr - 1] - 1]
                subdir = fullfile[subdir - 1, '*.crb.mat' - 1]
                res_files = dir[subdir - 1]
                
                if not isempty[res_files - 1]:
                    count1 = count1 + 1
                    (name1, end + 1)[] = (exp_struct, 'name')[ii_arr - 1]
                    array1 = np.array([[array1], [(exp_struct, 'array')[ii_arr - 1]]])
            res_exp_struct['count' - 1] = count1
            res_exp_struct['name' - 1] = name1
            res_exp_struct['array' - 1] = array1
            
            if count1 != 0:
                count_crb = count_crb + 1
                (name_crb, end + 1)[] = (dir_res_now_crb, 'name')[i_arr - 1]
                array_crb = np.array([[array_crb], [res_exp_struct]])
        exp_struct = dir_res_now_est['array'][i_arr - 1]
        
        if exp_struct['count'] != 0:
            res_exp_struct = struct
            count1 = 0
            name1 = [[]]
            array1 = None
            
            for ii_arr in np.arange(1, (exp_struct, 'count') + 1):
                subdir = fullfile['results' - 1, (dir_res_now_est, 'name')[i_arr - 1] - 1, (exp_struct, 'name')[ii_arr - 1] - 1]
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
                count_est = count_est + 1
                (name_est, end + 1)[] = (dir_res_now_est, 'name')[i_arr - 1]
                array_est = np.array([[array_est], [res_exp_struct]])
    dir_now_crb['count' - 1] = count_crb
    dir_now_crb['name' - 1] = name_crb
    dir_now_crb['array' - 1] = array_crb
    dir_now_est['count' - 1] = count_est
    dir_now_est['name' - 1] = name_est
    dir_now_est['array' - 1] = array_est
    defAns = struct
    sim_ind_crb = 1
    sim_ind_est = 1
    defAns['sim_name_crb' - 1] = dir_now_crb['name'][sim_ind_crb - 1]
    defAns['exp_name_crb' - 1] = (dir_now_crb, 'array')[sim_ind_crb - 1]['name'][1 - 1]
    defAns['sim_name_est' - 1] = dir_now_est['name'][sim_ind_est - 1]
    defAns['exp_name_est' - 1] = (dir_now_est, 'array')[sim_ind_est - 1]['name'][1 - 1]
    defAns['dataMetric' - 1] = 'DFO'
    md5 = GetMD5[dir_now_est - 1, 'Array' - 1]
    defVal_path = fullfile['_tmp' - 1, 'defaultInput_plot_crb.mat' - 1]
    
    if isfile[defVal_path - 1]:
        defVal = load[defVal_path - 1]['defVal']
        md5_prev = defVal['md5']
        
        if strcmp[md5 - 1, md5_prev - 1]:
            sim_ind_crb = defVal['sim_ind_crb']
            sim_ind_est = defVal['sim_ind_est']
            defAns = defVal['defAns']
        else:
            sim_ind_crb = 1
            sim_ind_est = 1
            defAns['sim_name_crb' - 1] = dir_now_crb['name'][sim_ind_crb - 1]
            defAns['exp_name_crb' - 1] = (dir_now_crb, 'array')[sim_ind_crb - 1]['name'][1 - 1]
            defAns['sim_name_est' - 1] = dir_now_est['name'][sim_ind_est - 1]
            defAns['exp_name_est' - 1] = (dir_now_est, 'array')[sim_ind_est - 1]['name'][1 - 1]
            defAns['dataMetric' - 1] = 'DFO'
    prompt = [[]]
    title = 'Plot setting'
    formats = [[]]
    options = struct
    prompt(1, :) = [['Enter CRB data name:', 'sim_name_crb', [[]]]]
    formats[1 - 1, 1 - 1]['type' - 1] = 'list'
    formats[1 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[1 - 1, 1 - 1]['size' - 1] = -1
    formats[1 - 1, 1 - 1]['format' - 1] = 'text'
    formats[1 - 1, 1 - 1]['items' - 1] = dir_now_crb['name']
    formats[1 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now_crb, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    prompt(2, :) = [['CRB experiment', 'exp_name_crb', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'list'
    formats[2 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[2 - 1, 1 - 1]['size' - 1] = -1
    formats[2 - 1, 1 - 1]['format' - 1] = 'text'
    formats[2 - 1, 1 - 1]['items' - 1] = (dir_now_crb, 'array')[sim_ind_crb - 1]['name']
    prompt(3, :) = [['Enter estimation data name:', 'sim_name_est', [[]]]]
    formats[3 - 1, 1 - 1]['type' - 1] = 'list'
    formats[3 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[3 - 1, 1 - 1]['size' - 1] = -1
    formats[3 - 1, 1 - 1]['format' - 1] = 'text'
    formats[3 - 1, 1 - 1]['items' - 1] = dir_now_est['name']
    formats[3 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now_est, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    prompt(4, :) = [['estimation experiment', 'exp_name_est', [[]]]]
    formats[4 - 1, 1 - 1]['type' - 1] = 'list'
    formats[4 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[4 - 1, 1 - 1]['size' - 1] = -1
    formats[4 - 1, 1 - 1]['format' - 1] = 'text'
    formats[4 - 1, 1 - 1]['items' - 1] = (dir_now_est, 'array')[sim_ind_est - 1]['name']
    prompt(5, :) = [['Enter data type: ', 'dataMetric', [[]]]]
    formats[5 - 1, 1 - 1]['type' - 1] = 'list'
    formats[5 - 1, 1 - 1]['style' - 1] = 'radiobutton'
    formats[5 - 1, 1 - 1]['size' - 1] = -1
    formats[5 - 1, 1 - 1]['format' - 1] = 'text'
    formats[5 - 1, 1 - 1]['items' - 1] = [['DFO', 'AOA']]
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    
    if IsCancelled == 0:
        answer['sim_name_crb' - 1] = (answer, 'sim_name_crb')[1 - 1]
        answer['sim_name_est' - 1] = (answer, 'sim_name_est')[1 - 1]
        defVal = struct
        defVal['md5' - 1] = md5
        sim_ind_crb = find[ismember[dir_now_crb['name'] - 1, answer['sim_name_crb'] - 1] - 1]
        sim_ind_est = find[ismember[dir_now_est['name'] - 1, answer['sim_name_est'] - 1] - 1]
        defVal['sim_ind_crb' - 1] = sim_ind_crb
        defVal['sim_ind_est' - 1] = sim_ind_est
        defVal['defAns' - 1] = answer
        
        if not exist['_tmp' - 1, 'dir' - 1]:
            mkdir['_tmp' - 1]
        save[defVal_path - 1, 'defVal' - 1]
    return answer[IsCancelled]