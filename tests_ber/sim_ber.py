import numpy as np
clc
clear
close
SHOW_PROGRESS = 1
SEED = 506
glob_flag = struct
algo_flag = struct
glob_flag['add_noise' - 1] = 1
glob_flag['enable_CP_sim' - 1] = 0
glob_flag['assume_known_channel' - 1] = 0
glob_flag['use_correct_dfo' - 1] = 0
glob_flag['use_correct_aoa' - 1] = 0
glob_flag['use_correct_chl' - 1] = 0
algo_flag['equalizer' - 1] = 'MMSE'
algo_flag['assume_no_dfo' - 1] = 0
algo_flag['assume_no_aoa' - 1] = 0
algo_flag['post' - 1] = 'NONE'

if strcmpi[algo_flag['equalizer'] - 1, 'ZF' - 1]:
    pass
elif strcmpi[algo_flag['equalizer'] - 1, 'MMSE' - 1]:
    algo_flag['equ_opt' - 1, 'use_correct_snr' - 1] = 0
    algo_flag['equ_opt' - 1, 'compute_snr_each_datablock' - 1] = 0
else:
    error['wrong equalizer' - 1]

if strcmpi[algo_flag['post'] - 1, 'NONE' - 1]:
    pass
elif strcmpi[algo_flag['post'] - 1, 'ML_SEARCH' - 1]:
    algo_flag['post_opt' - 1, 'thres' - 1] = 0.01
    algo_flag['post_opt' - 1, 'max_error_symbol_number' - 1] = 5
else:
    error['wrong post-processing method' - 1]

if glob_flag['assume_known_channel'] == 1:
    glob_flag['use_correct_dfo' - 1] = 1
    glob_flag['use_correct_aoa' - 1] = 1
    glob_flag['use_correct_chl' - 1] = 1
glob_flag['gen_chl_mtx_flags' - 1] = uint8[0 - 1]

if glob_flag['use_correct_dfo'] == 1:
    glob_flag['gen_chl_mtx_flags' - 1] = bitset[glob_flag['gen_chl_mtx_flags'] - 1, 1 - 1, 1 - 1]

if glob_flag['use_correct_aoa'] == 1:
    glob_flag['gen_chl_mtx_flags' - 1] = bitset[glob_flag['gen_chl_mtx_flags'] - 1, 2 - 1, 1 - 1]

if glob_flag['use_correct_chl'] == 1:
    glob_flag['gen_chl_mtx_flags' - 1] = bitset[glob_flag['gen_chl_mtx_flags'] - 1, 3 - 1, 1 - 1]

if glob_flag['add_noise'] == 0:
    warning['noise free' - 1]

if glob_flag['assume_known_channel'] == 1:
    warning['ideal case simulation' - 1]

if glob_flag['use_correct_dfo'] == 1:
    warning['use correct DFO' - 1]

if glob_flag['use_correct_aoa'] == 1:
    warning['use correct AoA' - 1]

if glob_flag['use_correct_chl'] == 1:
    warning['use correct channel' - 1]

if algo_flag['assume_no_dfo'] == 1:
    warning['receiver ignores DFO' - 1]

if algo_flag['assume_no_aoa'] == 1:
    warning['receiver ignores AoA' - 1]
addpath[genpath['src' - 1] - 1]
default_sim_Mc = 5000
default_sim_snr = np.arange(-10, 40 + 10, 10)
default_sim_Q = np.arange(1, 5 + 1)
default_sim_Nr = 1
default_exp_name = 'first try'
answer['IsCancelled'] = request_user_input_sim_ber[default_sim_Mc - 1, default_exp_name - 1]

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
est_config_name = sprintf['%s_sim_config.est.mat' - 1, sim_name - 1]
est_config = load[fullfile['_sim_result_est' - 1, dir_exp - 1, est_config_name - 1] - 1]
Mc = min[np.array([[default_sim_Mc, (gen_config, 'Mc'), (est_config, 'Mc')]]) - 1]
snr['unmatched_snr'] = intersects[default_sim_snr - 1, gen_config['snr'] - 1, est_config['snr'] - 1]

if unmatched_snr:
    warning['different simulation snr setting' - 1]
snr_gendata_idx = arrcmp[snr - 1, gen_config['snr'] - 1, 1 - 1]
snr_estchal_idx = arrcmp[snr - 1, est_config['snr'] - 1, 1 - 1]
Q['unmatched_Q'] = intersects[default_sim_Q - 1, gen_config['Q'] - 1, est_config['Q'] - 1]

if unmatched_Q:
    warning['different simulation Q setting' - 1]
Q_gendata_idx = arrcmp[Q - 1, gen_config['Q'] - 1, 1 - 1]
Q_estchal_idx = arrcmp[Q - 1, est_config['Q'] - 1, 1 - 1]
Nr = default_sim_Nr

if Nr != est_config['Nr']:
    error['different simulation Nr setting' - 1]
dir_dump = fullfile['_dump' - 1, dir_sim - 1]

if not exist[dir_dump - 1, 'dir' - 1]:
    mkdir[dir_dump - 1]
n_snr = length[snr - 1]
n_Q = length[Q - 1]
sim_Mc_info = struct
sim_Mc_info['snr' - 1] = snr
sim_Mc_info['Q' - 1] = Q
sim_Mc_info['Nr' - 1] = Nr
sim_Mc_info['config' - 1] = config
sim_Mc_info['glob_flag' - 1] = glob_flag
sim_Mc_info['algo_flag' - 1] = algo_flag
sim_Mc_info['dir_gendata' - 1] = fullfile['_gendata' - 1, sim_name - 1, sim_name - 1]
sim_Mc_info['dir_estdata' - 1] = fullfile['_sim_result_est' - 1, dir_exp - 1, sim_name - 1]
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
fprintf[1 - 1, 'Simulation info:\\n' - 1]
fprintf[1 - 1, '\\tsim_src:\\t%s\\n' - 1, sim_name - 1]
fprintf[1 - 1, '\\texp_src:\\t%s\\n' - 1, exp_name - 1]
fprintf[1 - 1, '\\texp_name:\\t%s\\n' - 1, sub_trial - 1]
fprintf[1 - 1, '\\tMc\\t=\\t%d\\n' - 1, Mc - 1]
fprintf[1 - 1, '\\tQ\\t=\\t[%s]\\n' - 1, join[string[Q - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tsnr\\t=\\t[%s]\\n' - 1, join[string[snr - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tNr\\t=\\t%d\\n' - 1, Nr - 1]
fprintf[1 - 1, 'Start simulation at %s\\n' - 1, string[datetime['now' - 1] - 1] - 1]
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]

if SHOW_PROGRESS == 1:
    PB = ProgressBar_cli_parfor[Mc - 1]
tic

for i_Mc in np.arange(1, Mc + 1):
    stream = prngsc['Value']
    stream['Substream' - 1] = i_Mc
    RandStream['setGlobalStream'][stream - 1]
    path_full_name = sprintf['%s_avg_ber_%03d.ber.mat' - 1, sim_name - 1, i_Mc - 1]
    path_full = fullfile[dir_dump - 1, path_full_name - 1]
    
    if sim_mode >= 2:
        
        if isfile[path_full - 1]:
            data = load[path_full - 1]
            r_avg_ber = data['r_avg_ber']
            load_Q['unmatched_Q'] = intersects[Q - 1, data['Q'] - 1]
            load_snr['unmatched_snr'] = intersects[snr - 1, data['snr'] - 1]
            
            if unmatched_snr or unmatched_Q:
                load_Q_idx = arrcmp[load_Q - 1, data['Q'] - 1, 1 - 1]
                load_snr_idx = arrcmp[load_snr - 1, data['snr'] - 1, 1 - 1]
                r_avg_ber_Mc(:, :, i_Mc) = r_avg_ber[load_Q_idx - 1, load_snr_idx - 1]
            else:
                r_avg_ber_Mc(:, :, i_Mc) = r_avg_ber
        else:
            valid_Mc(i_Mc) = 0
    elif sim_mode >= 1 and isfile[path_full - 1]:
        data = load[path_full - 1]
        r_avg_ber = data['r_avg_ber']
        load_snr['unmatched_snr'] = intersects[snr - 1, data['snr'] - 1]
        load_Q['unmatched_Q'] = intersects[Q - 1, data['Q'] - 1]
        
        if unmatched_snr or unmatched_Q:
            load_Q_idx = arrcmp[load_Q - 1, data['Q'] - 1, 1 - 1]
            load_snr_idx = arrcmp[load_snr - 1, data['snr'] - 1, 1 - 1]
            r_avg_ber_Mc(:, :, i_Mc) = r_avg_ber[load_Q_idx - 1, load_snr_idx - 1]
        else:
            r_avg_ber_Mc(:, :, i_Mc) = r_avg_ber
    else:
        r_avg_ber = one_Mc_ber[i_Mc - 1, psimset['Value'] - 1]
        r_avg_ber_Mc(:, :, i_Mc) = r_avg_ber
        parsave[path_full - 1, r_avg_ber - 1, Q - 1, snr - 1, Nr - 1]
    
    if SHOW_PROGRESS == 1:
        advance[PB - 1]
fprintf[1 - 1, 'done!\\n' - 1]
sim_exe_time = toc
fprintf[1 - 1, '\\nexecution time: %s\\n' - 1, show_duration[sim_exe_time - 1] - 1]
avg_ber = squeeze[sum[r_avg_ber_Mc - 1, 3 - 1] / nnz[valid_Mc - 1] - 1]
Mc = nnz[valid_Mc - 1]
dir_result = fullfile['results' - 1, dir_sim - 1]

if not exist[dir_result - 1, 'dir' - 1]:
    mkdir[dir_result - 1]
path_full_name = sprintf['%s_channel_config.ber.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'config' - 1]
path_full_name = sprintf['%s_sim_config.ber.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'Mc' - 1, 'Q' - 1, 'snr' - 1, 'Nr' - 1, 'sim_exe_time' - 1]
path_full_name = sprintf['%s_avg_ber.ber.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'avg_ber' - 1]