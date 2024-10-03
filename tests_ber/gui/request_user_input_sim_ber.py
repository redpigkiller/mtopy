import numpy as np


def request_user_input_sim_ber(default_Mc, default_exp_name):
    dir_gen_now = get_subfolders_r['_gendata' - 1, 2 - 1]
    
    if dir_gen_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation source.\\n' + 'Please execute gen_cases.m first!\\n' - 1]
        
        return
    dir_sim_now = get_subfolders_r['_sim_result_est' - 1, 3 - 1]
    
    if dir_sim_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation results.\\n' + 'Please execute sim_estimate_channel.m first!\\n' - 1]
        
        return
    dir_now = struct
    tmp_names = intersect[dir_gen_now['name'] - 1, dir_sim_now['name'] - 1]
    tmp_name_idx = np.zeros((length[tmp_names - 1], 1))
    
    for i_name in np.arange(1, length[tmp_names - 1] + 1):
        name = tmp_names[i_name - 1]
        tmp_name_idx(i_name) = find[strcmp[dir_sim_now['name'] - 1, name - 1] - 1]
    tmp_name_idx(tmp_name_idx == 0) = None
    tmp_name_idx = sort[tmp_name_idx - 1]
    count = 0
    name = [[]]
    array = None
    
    for i_arr in np.arange(1, length[tmp_name_idx - 1] + 1):
        exp_struct = dir_sim_now['array'][tmp_name_idx[i_arr - 1] - 1]
        
        if exp_struct['count'] != 0:
            count = count + 1
            (name, end + 1)[] = (dir_sim_now, 'name')[tmp_name_idx[i_arr - 1] - 1]
            array = np.array([[array], [exp_struct]])
    dir_now['count' - 1] = count
    dir_now['name' - 1] = name
    dir_now['array' - 1] = array
    defInd = struct
    defInd['i_sim_src' - 1] = 1
    defInd['i_exp_src' - 1] = 1
    defAns = struct
    defAns['Mc' - 1] = default_Mc
    defAns['exp_name' - 1] = default_exp_name
    defAns['flag_collect_mode' - 1] = false
    defAns['flag_skip_simulated' - 1] = true
    defAns['flag_use_parfor' - 1] = true
    defAns['flag_use_gpu' - 1] = false
    md5 = GetMD5[dir_now - 1, 'Array' - 1]
    defVal_path = fullfile['_tmp' - 1, 'defaultInput_sim_ber.mat' - 1]
    
    if isfile[defVal_path - 1]:
        defVal = load[defVal_path - 1]['defVal']
        md5_prev = defVal['md5']
        
        if strcmp[md5 - 1, md5_prev - 1]:
            defInd = defVal['defInd']
            defAns = defVal['defAns']
        else:
            defAns['exp_name' - 1] = defVal['defAns']['exp_name']
            defAns['flag_collect_mode' - 1] = defVal['defAns']['flag_collect_mode']
            defAns['flag_skip_simulated' - 1] = defVal['defAns']['flag_skip_simulated']
            defAns['flag_use_parfor' - 1] = defVal['defAns']['flag_use_parfor']
            defAns['flag_use_gpu' - 1] = defVal['defAns']['flag_use_gpu']
    defAns['sim_src_name' - 1] = dir_now['name'][defInd['i_sim_src'] - 1]
    defAns['exp_src_name' - 1] = (dir_now, 'array')[(defInd, 'i_sim_src') - 1]['name'][defInd['i_exp_src'] - 1]
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
    formats[1 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    formats[1 - 1, 1 - 1]['span' - 1] = np.array([[1, 4]])
    prompt(2, :) = [['Enter experiment source:', 'exp_src_name', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'list'
    formats[2 - 1, 1 - 1]['style' - 1] = 'popupmenu'
    formats[2 - 1, 1 - 1]['size' - 1] = -1
    formats[2 - 1, 1 - 1]['format' - 1] = 'text'
    formats[2 - 1, 1 - 1]['items' - 1] = (dir_now, 'array')[(defInd, 'i_sim_src') - 1]['name']
    formats[2 - 1, 1 - 1]['span' - 1] = np.array([[1, 4]])
    prompt(3, :) = [['number of simulation trials', 'Mc', [[]]]]
    formats[3 - 1, 1 - 1]['type' - 1] = 'edit'
    formats[3 - 1, 1 - 1]['size' - 1] = -1
    formats[3 - 1, 1 - 1]['format' - 1] = 'integer'
    formats[3 - 1, 1 - 1]['span' - 1] = np.array([[1, 4]])
    prompt(4, :) = [['experiment', 'exp_name', [[]]]]
    formats[4 - 1, 1 - 1]['type' - 1] = 'edit'
    formats[4 - 1, 1 - 1]['size' - 1] = -1
    formats[4 - 1, 1 - 1]['format' - 1] = 'text'
    formats[4 - 1, 1 - 1]['span' - 1] = np.array([[1, 4]])
    prompt(5, :) = [['collect mode', 'flag_collect_mode', [[]]]]
    formats[5 - 1, 1 - 1]['type' - 1] = 'check'
    prompt(6, :) = [['skip simulated', 'flag_skip_simulated', [[]]]]
    formats[5 - 1, 2 - 1]['type' - 1] = 'check'
    prompt(7, :) = [['use parfor', 'flag_use_parfor', [[]]]]
    formats[5 - 1, 3 - 1]['type' - 1] = 'check'
    prompt(8, :) = [['use GPU', 'flag_use_gpu', [[]]]]
    formats[5 - 1, 4 - 1]['type' - 1] = 'check'
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    
    if IsCancelled == 0:
        answer['sim_src_name' - 1] = (answer, 'sim_src_name')[1 - 1]
        answer['exp_src_name' - 1] = (answer, 'exp_src_name')[1 - 1]
        defVal = struct
        defVal['md5' - 1] = md5
        ind = struct
        ind['i_sim_src' - 1] = find[ismember[dir_now['name'] - 1, answer['sim_src_name'] - 1] - 1]
        ind['i_exp_src' - 1] = find[ismember[(dir_now, 'array')[(ind, 'i_sim_src') - 1]['name'] - 1, answer['exp_src_name'] - 1] - 1]
        defVal['defInd' - 1] = ind
        defVal['defAns' - 1] = answer
        
        if not exist['_tmp' - 1, 'dir' - 1]:
            mkdir['_tmp' - 1]
        save[defVal_path - 1, 'defVal' - 1]
    return answer[IsCancelled]