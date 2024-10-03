import numpy as np
clc
clear
close
SHOW_PROGRESS = 0
SEED = 506
glob_flag = struct
algo_flag = struct
glob_flag['add_noise' - 1] = 1
glob_flag['assume_known_channel' - 1] = 0
glob_flag['use_correct_dfo' - 1] = 0
glob_flag['use_correct_chl' - 1] = 0
algo_flag['position' - 1] = 1
algo_flag['null_subcarrier' - 1] = 0
algo_flag['equalizer' - 1] = 'MMSE'
algo_flag['assume_no_dfo' - 1] = 0

if strcmpi[algo_flag['equalizer'] - 1, 'ZF' - 1]:
    pass
elif strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1]:
    algo_flag['equ_opt' - 1, 'use_correct_snr' - 1] = 0
    algo_flag['equ_opt' - 1, 'compute_snr_each_datablock' - 1] = 0
else:
    error['wrong equalizer' - 1]

if glob_flag['assume_known_channel'] == 1:
    glob_flag['use_correct_dfo' - 1] = 1
    glob_flag['use_correct_chl' - 1] = 1
addpath[genpath['src' - 1] - 1]
default_sim_Mc = 10
default_sim_snr = 40
default_sim_Q = np.arange(1, 4 + 1)
default_exp_name = 'first try'
answer['IsCancelled'] = request_user_input(default_sim_Mc, default_exp_name)

if IsCancelled:
    
    return
glob_flag['use_gpu' - 1] = answer['flag_use_gpu']
glob_flag['use_parfor' - 1] = answer['flag_use_parfor']
glob_flag['skip_simulated' - 1] = answer['flag_skip_simulated']
glob_flag['collect_mode' - 1] = answer['flag_collect_mode']
sim_name = answer['sim_src_name']
exp_name = answer['exp_src_name']
default_sim_Mc = answer['Mc']
sub_trial = answer['exp_name']
dir_exp = fullfile[sim_name - 1, exp_name - 1]
dir_sim = fullfile[sim_name - 1, sub_trial - 1]
config_name = sprintf['%s_config.mat' - 1, sim_name - 1]
config = load[fullfile['_gendata' - 1, sim_name - 1, config_name - 1] - 1]['config']
gen_config_name = sprintf['%s_gen_config.mat' - 1, sim_name - 1]
gen_config = load[fullfile['_gendata' - 1, sim_name - 1, gen_config_name - 1] - 1]
est_config_name = sprintf['%s_sim_config.chl.mat' - 1, sim_name - 1]
est_config = load[fullfile['_simResult_est_dfo_chl' - 1, dir_exp - 1, est_config_name - 1] - 1]
Mc = min[np.array([[default_sim_Mc, (gen_config, 'Mc'), (est_config, 'Mc')]]) - 1]
snr['unmatched_snr'] = intersects[default_sim_snr - 1, gen_config['snr'] - 1, est_config['snr'] - 1]

if unmatched_snr:
    warning['different simulation snr setting' - 1]
snr_gendata_idx = cmp_arr[snr - 1, gen_config['snr'] - 1, 1 - 1]
snr_estchal_idx = cmp_arr[snr - 1, est_config['snr'] - 1, 1 - 1]
Q['unmatched_Q'] = intersects[default_sim_Q - 1, gen_config['Q'] - 1, est_config['Q'] - 1]

if unmatched_Q:
    warning['different simulation Q setting' - 1]
Q_gendata_idx = cmp_arr[Q - 1, gen_config['Q'] - 1, 1 - 1]
Q_estchal_idx = cmp_arr[Q - 1, est_config['Q'] - 1, 1 - 1]
dir_dump = fullfile['_exp_dump' - 1, dir_sim - 1]

if not exist[dir_dump - 1, 'dir' - 1]:
    mkdir[dir_dump - 1]
n_snr = length[snr - 1]
n_Q = length[Q - 1]
sim_Mc_info = struct
sim_Mc_info['snr' - 1] = snr
sim_Mc_info['Q' - 1] = Q
sim_Mc_info['config' - 1] = config
sim_Mc_info['glob_flag' - 1] = glob_flag
sim_Mc_info['algo_flag' - 1] = algo_flag
sim_Mc_info['dir_gendata' - 1] = fullfile['_gendata' - 1, sim_name - 1, sim_name - 1]
sim_Mc_info['dir_estdata' - 1] = fullfile['_simResult_est_dfo_chl' - 1, dir_exp - 1, sim_name - 1]
sim_Mc_info['snr_gendata_idx' - 1] = snr_gendata_idx
sim_Mc_info['snr_estchal_idx' - 1] = snr_estchal_idx
sim_Mc_info['Q_gendata_idx' - 1] = Q_gendata_idx
sim_Mc_info['Q_estchal_idx' - 1] = Q_estchal_idx
r_avg_ber_Mc = np.zeros((n_Q, n_snr, Mc))

if glob_flag['use_parfor'] != 0:
    poolobj = startparpool[]
    parforArg = poolobj['NumWorkers']
else:
    parforArg = 0
prngsc = parallel['pool']['Constant'][RandStream['Threefry' - 1, 'Seed' - 1, SEED - 1] - 1]
psimset = parallel['pool']['Constant'][sim_Mc_info - 1]
sim_mode = 2 @ glob_flag['collect_mode'] + glob_flag['skip_simulated']
valid_Mc = np.ones((Mc, 1))
fprintf[1 - 1, 'Start simulation with exp_name: %s\\n' - 1, sub_trial - 1]

if SHOW_PROGRESS == 1:
    parfor_progress[Mc - 1]
tic

for i_Mc in np.arange(1, Mc + 1):
    stream = prngsc['Value']
    stream['Substream' - 1] = i_Mc
    RandStream['setGlobalStream'][stream - 1]
    path_full_name = sprintf['%s_r_avg_ber_%03d.ber.mat' - 1, sim_name - 1, i_Mc - 1]
    path_full = fullfile[dir_dump - 1, path_full_name - 1]
    
    if sim_mode >= 2:
        
        if isfile[path_full - 1]:
            pass
        else:
            valid_Mc(i_Mc) = 0
    elif sim_mode >= 1 and isfile[path_full - 1]:
        pass
    else:
        r_eZF_Mc['r_eMMSE_Mc']['r_eCORR_Mc'] = exp_one_Mc_ber[i_Mc - 1, psimset['Value'] - 1]
        parsave[path_full - 1, r_eZF_Mc - 1, r_eMMSE_Mc - 1, r_eCORR_Mc - 1, Q - 1, snr - 1]
    
    if SHOW_PROGRESS == 1:
        parfor_progress

if SHOW_PROGRESS == 1:
    parfor_progress[0 - 1]
fprintf[1 - 1, 'done!\\n' - 1]
sim_exe_time = toc
fprintf[1 - 1, '\\nexecution time: %s\\n' - 1, show_duration[sim_exe_time - 1] - 1]


def request_user_input(default_Mc, default_exp_name):
    dir_gen_now = get_subfolders_r['_gendata' - 1, 2 - 1]
    
    if dir_gen_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation source.\\n' + 'Please execute gen_cases.m first!' - 1]
        
        return
    dir_sim_now = get_subfolders_r['_simResult_est_dfo_chl' - 1, 3 - 1]
    
    if dir_sim_now['count'] == 0:
        answer = struct
        IsCancelled = 1
        fprintf[1 - 1, 'Can not find any simulation results.\\n' + 'Please execute sim_estimate_channel.m first!' - 1]
        
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