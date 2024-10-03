import numpy as np
addpath[genpath['src' - 1] - 1]
answer['IsCancelled'] = request_user_input()

if IsCancelled == 1:
    
    return
remove_dir(answer['sim_src'], answer['sim_exp'])


def request_user_input():
    dir_dmp_now = get_subfolders_r['_dump' - 1, 2 - 1]
    
    if dir_dmp_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation.\\n' - 1]
        
        return
    dir_now = struct
    count = 0
    name = [[]]
    array = None
    
    for i_arr in np.arange(1, (dir_dmp_now, 'count') + 1):
        exp_struct = dir_dmp_now['array'][i_arr - 1]
        
        if exp_struct['count'] != 0:
            count = count + 1
            (name, end + 1)[] = (dir_dmp_now, 'name')[i_arr - 1]
            array = np.array([[array], [exp_struct]])
    dir_now['count' - 1] = count
    dir_now['name' - 1] = name
    dir_now['array' - 1] = array
    defAns = struct
    defAns['sim_src' - 1] = dir_now['name'][1 - 1]
    defAns['sim_exp' - 1] = (dir_now, 'array')[1 - 1]['name'][1 - 1]
    prompt = [[]]
    title = 'Remove simulation data'
    formats = [[]]
    options = struct
    prompt(1, :) = [['Simulation source:', 'sim_src', [[]]]]
    formats[1 - 1, 1 - 1]['type' - 1] = 'list'
    formats[1 - 1, 1 - 1]['style' - 1] = 'listbox'
    formats[1 - 1, 1 - 1]['size' - 1] = np.array([[0, 200]])
    formats[1 - 1, 1 - 1]['format' - 1] = 'text'
    formats[1 - 1, 1 - 1]['items' - 1] = dir_now['name']
    formats[1 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    prompt(2, :) = [['Simulation experiment:', 'sim_exp', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'list'
    formats[2 - 1, 1 - 1]['style' - 1] = 'listbox'
    formats[2 - 1, 1 - 1]['size' - 1] = np.array([[0, 200]])
    formats[2 - 1, 1 - 1]['format' - 1] = 'text'
    formats[2 - 1, 1 - 1]['items' - 1] = (dir_now, 'array')[1 - 1]['name']
    formats[2 - 1, 1 - 1]['limits' - 1] = np.array([[0, 2]])
    options['Resize' - 1] = 'on'
    options['AlignControls' - 1] = 'on'
    options['ButtonNames' - 1] = [['Continue for sure?', 'Cancel']]
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    return answer[IsCancelled]


def remove_dir(sim_src, sim_exp):
    answer = questdlg['remove for sure?' - 1, 'double check' - 1, 'yes' - 1, 'no' - 1, 'no' - 1]
    
    if answer == 'yes':
        sim_name = sim_src[1 - 1]
        dump_dir = fullfile['_dump' - 1, sim_name - 1]
        save_dir = fullfile['_sim_result_est' - 1, sim_name - 1]
        res_dir = fullfile['results' - 1, sim_name - 1]
        fig_dir = fullfile['figure' - 1, sim_name - 1]
        
        for idx in np.arange(1, length[sim_exp - 1] + 1):
            full_path = fullfile[dump_dir - 1, sim_exp[idx - 1] - 1]
            status = rmdir[full_path - 1, 's' - 1]
            full_path = fullfile[save_dir - 1, sim_exp[idx - 1] - 1]
            status = rmdir[full_path - 1, 's' - 1]
            full_path = fullfile[res_dir - 1, sim_exp[idx - 1] - 1]
            status = rmdir[full_path - 1, 's' - 1]
            full_path = fullfile[fig_dir - 1, sim_exp[idx - 1] - 1]
            status = rmdir[full_path - 1, 's' - 1]
    elif answer == 'no':
        pass
    else:
        pass