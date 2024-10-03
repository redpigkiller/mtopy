import numpy as np


def request_user_input_sim_crb(default_Mc, default_exp_name):
    dir_now = get_subfolders_r['_gendata' - 1, 2 - 1]
    
    if dir_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation source.\\n' + 'Please execute gen_cases.m first!\\n' - 1]
        
        return
    defAns = struct
    defAns['sim_src_name' - 1] = dir_now['name'][1 - 1]
    defAns['exp_name' - 1] = default_exp_name
    defAns['Mc' - 1] = default_Mc
    defAns['flag_use_parfor' - 1] = true
    md5 = GetMD5[dir_now - 1, 'Array' - 1]
    defVal_path = fullfile['_tmp' - 1, 'defaultInput_sim_crb.mat' - 1]
    
    if isfile[defVal_path - 1]:
        defVal = load[defVal_path - 1]['defVal']
        md5_prev = defVal['md5']
        
        if strcmp[md5 - 1, md5_prev - 1]:
            defAns = defVal['defAns']
        else:
            defAns['exp_name' - 1] = defVal['defAns']['exp_name']
            defAns['flag_use_parfor' - 1] = defVal['defAns']['flag_use_parfor']
    prompt = [[]]
    title = 'Simulation setting'
    formats = [[]]
    options = struct
    prompt(1, :) = [['Enter simulation data source:', 'sim_src_name', [[]]]]
    formats[1 - 1, 1 - 1]['type' - 1] = 'list'
    formats[1 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[1 - 1, 1 - 1]['size' - 1] = -1
    formats[1 - 1, 1 - 1]['format' - 1] = 'text'
    formats[1 - 1, 1 - 1]['items' - 1] = dir_now['name']
    prompt(2, :) = [['number of simulation trials', 'Mc', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'edit'
    formats[2 - 1, 1 - 1]['size' - 1] = -1
    formats[2 - 1, 1 - 1]['format' - 1] = 'integer'
    prompt(3, :) = [['experiment', 'exp_name', [[]]]]
    formats[3 - 1, 1 - 1]['type' - 1] = 'edit'
    formats[3 - 1, 1 - 1]['size' - 1] = -1
    formats[3 - 1, 1 - 1]['format' - 1] = 'text'
    prompt(4, :) = [['use parfor', 'flag_use_parfor', [[]]]]
    formats[4 - 1, 1 - 1]['type' - 1] = 'check'
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    
    if IsCancelled == 0:
        answer['sim_src_name' - 1] = (answer, 'sim_src_name')[1 - 1]
        defVal = struct
        defVal['md5' - 1] = md5
        defVal['defAns' - 1] = answer
        
        if not exist['_tmp' - 1, 'dir' - 1]:
            mkdir['_tmp' - 1]
        save[defVal_path - 1, 'defVal' - 1]
    return answer[IsCancelled]