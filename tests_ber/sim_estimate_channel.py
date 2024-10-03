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
algo_flag['estimate_dfo' - 1] = 1
algo_flag['estimate_chl' - 1] = 0
algo_flag['use_dfo_aoa_algo' - 1] = 'ML_Estimation'
algo_flag['enable_sep' - 1] = true
algo_flag['use_chl_algo_stage_1' - 1] = 'TIKHONOV'
algo_flag['use_chl_algo_stage_2' - 1] = 'PINV'

if strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'ESPRIT' - 1]:
    algo_flag['dfo_opt' - 1, 'minus_mean' - 1] = 0
    algo_flag['dfo_opt' - 1, 'sig_subspace' - 1] = 'SVD'
    algo_flag['dfo_opt' - 1, 'method' - 1] = 'TLS'
elif strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'UNITARY_ESPRIT' - 1]:
    algo_flag['dfo_opt' - 1, 'sig_subspace' - 1] = 'SVD'
    algo_flag['dfo_opt' - 1, 'method' - 1] = 'TLS'
elif strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'ML_Estimation' - 1]:
    algo_flag['dfo_opt' - 1, 'algo' - 1] = 'PSO'
    algo_flag['dfo_opt' - 1, 'algoOpt' - 1] = lambda Q: iif[(Q == 1) - 1, 'b' - 1, 'b' - 1]
    algo_flag['dfo_opt' - 1, 'method' - 1] = lambda Q: iif[(Q == 1) - 1, 1 - 1, 1 - 1]
elif strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'UNITARY_ESPRIT_2D' - 1]:
    algo_flag['dfo_aoa_opt' - 1, 'sig_subspace' - 1] = 'SVD'
    algo_flag['dfo_aoa_opt' - 1, 'method' - 1] = 'TLS'
else:
    error['wrong DFO algorithm' - 1]

if strcmpi[algo_flag['use_chl_algo_stage_1'] - 1, 'PINV' - 1]:
    pass
elif strcmpi[algo_flag['use_chl_algo_stage_1'] - 1, 'TIKHONOV' - 1]:
    algo_flag['chl_opt_stage_1' - 1, 'reg' - 1] = 0.001
elif strcmpi[algo_flag['use_chl_algo_stage_1'] - 1, 'PINV_KRON' - 1]:
    pass
elif strcmpi[algo_flag['use_chl_algo_stage_1'] - 1, 'TIKHONOV_KRON' - 1]:
    algo_flag['chl_opt_stage_1' - 1, 'reg' - 1] = 0.001
else:
    error['wrong Channel stage 1 algorithm' - 1]

if strcmpi[algo_flag['use_chl_algo_stage_2'] - 1, 'PINV' - 1]:
    pass
elif strcmpi[algo_flag['use_chl_algo_stage_2'] - 1, 'MMSE' - 1]:
    algo_flag['chl_opt_stage_2' - 1, 'chlpwr' - 1] = 0.3
elif strcmpi[algo_flag['use_chl_algo_stage_2'] - 1, 'CS' - 1]:
    algo_flag['chl_opt_stage_2' - 1, 'chllen' - 1] = 5
else:
    error['wrong Channel stage 2 algorithm' - 1]

if glob_flag['add_noise'] == 0:
    warning['noise free' - 1]

if algo_flag['estimate_dfo'] == 0:
    warning['no DFO estimation' - 1]

if algo_flag['estimate_chl'] == 0:
    warning['no channel estimation' - 1]
addpath[genpath['src' - 1] - 1]
default_sim_Mc = 5000
default_sim_snr = np.arange(-10, 40 + 10, 10)
default_sim_Q = np.arange(1, 5 + 1)
default_sim_P = 8
default_sim_Nr = 1
N_ratio = 8
default_exp_name = 'first try'
answer['IsCancelled'] = request_user_input_sim_estimate[default_sim_Mc - 1, default_exp_name - 1]

if IsCancelled:
    
    return
glob_flag['use_parfor' - 1] = answer['flag_use_parfor']
glob_flag['use_gpu' - 1] = answer['flag_use_gpu']

if strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'ML_Estimation' - 1] and glob_flag['use_gpu']:
    glob_flag['use_gpu' - 1] = 0
    warning['ML_Estimation does NOT support GPU! Continue using CPU...' - 1]
glob_flag['skip_simulated' - 1] = answer['flag_skip_simulated']
glob_flag['collect_mode' - 1] = answer['flag_collect_mode']
sim_name = answer['sim_src_name']
default_sim_Mc = answer['Mc']
sub_trial = answer['exp_name']
dir_sim = fullfile[sim_name - 1, sub_trial - 1]
config_name = sprintf['%s_config.mat' - 1, sim_name - 1]
config = load[fullfile['_gendata' - 1, sim_name - 1, config_name - 1] - 1]['config']
gen_config_name = sprintf['%s_gen_config.mat' - 1, sim_name - 1]
gen_config = load[fullfile['_gendata' - 1, sim_name - 1, gen_config_name - 1] - 1]
sim_Mc = gen_config['Mc']
sim_snr = gen_config['snr']
sim_Q = gen_config['Q']
Mc = min[np.array([[default_sim_Mc, sim_Mc]]) - 1]
snr['unmatched_snr'] = intersects[default_sim_snr - 1, sim_snr - 1]

if unmatched_snr:
    warning['different simulation snr setting' - 1]
snr_idx = arrcmp[snr - 1, sim_snr - 1, 1 - 1]
Q['unmatched_Q'] = intersects[default_sim_Q - 1, sim_Q - 1]

if unmatched_Q:
    warning['different simulation Q setting' - 1]
Q_idx = arrcmp[Q - 1, sim_Q - 1, 1 - 1]
Nr = default_sim_Nr

if Nr > 1 and (not strcmpi[algo_flag['use_dfo_aoa_algo'] - 1, 'UNITARY_ESPRIT_2D' - 1]):
    error['Can not use 1D algorithm to estimate a 2D problem!' - 1]
P = default_sim_P
dir_dump = fullfile['_dump' - 1, dir_sim - 1]

if not exist[dir_dump - 1, 'dir' - 1]:
    mkdir[dir_dump - 1]
dir_save = fullfile['_sim_result_est' - 1, dir_sim - 1]

if not exist[dir_save - 1, 'dir' - 1]:
    mkdir[dir_save - 1]
n_snr = length[snr - 1]
n_Q = length[Q - 1]
sim_Mc_info = struct
sim_Mc_info['snr' - 1] = snr
sim_Mc_info['Q' - 1] = Q
sim_Mc_info['P' - 1] = P
sim_Mc_info['Nr' - 1] = Nr
sim_Mc_info['config' - 1] = config

if N_ratio != 1:
    sim_Mc_info['config' - 1, 'N' - 1] = sim_Mc_info['config']['N'] @ N_ratio
    warning['N_ratio != 1' - 1]
sim_Mc_info['glob_flag' - 1] = glob_flag
sim_Mc_info['algo_flag' - 1] = algo_flag
sim_Mc_info['dir_gendata' - 1] = fullfile['_gendata' - 1, sim_name - 1, sim_name - 1]
sim_Mc_info['snr_idx' - 1] = snr_idx
sim_Mc_info['Q_idx' - 1] = Q_idx
r_MSE_dfo_Mc = np.zeros((n_Q, n_snr, Mc))
r_MSE_aoa_Mc = np.zeros((n_Q, n_snr, Mc))
r_MSE_chl_Mc = np.zeros((n_Q, n_snr, Mc))
s_est_dfo_Mc = cell[n_Q - 1, n_snr - 1, Mc - 1]
s_est_aoa_Mc = cell[n_Q - 1, n_snr - 1, Mc - 1]
s_est_chl_Mc = cell[n_Q - 1, n_snr - 1, Mc - 1]

if glob_flag['use_parfor'] != 0:
    poolobj = startparpool[]
    parforArg = poolobj['NumWorkers']
else:
    parforArg = 0
prngsc = parallel['pool']['Constant'][RandStream['Threefry' - 1, 'Seed' - 1, SEED - 1] - 1]
psimset = parallel['pool']['Constant'][sim_Mc_info - 1]
sim_mode = 2 @ glob_flag['collect_mode'] + glob_flag['skip_simulated']
valid_Q_Mc = np.zeros((n_Q, Mc))
valid_snr_Mc = np.zeros((n_snr, Mc))
fprintf[1 - 1, 'Simulation info:\\n' - 1]
fprintf[1 - 1, '\\tsim_src:\\t%s\\n' - 1, sim_name - 1]
fprintf[1 - 1, '\\texp_name:\\t%s\\n' - 1, sub_trial - 1]
fprintf[1 - 1, '\\tMc\\t=\\t%d\\n' - 1, Mc - 1]
fprintf[1 - 1, '\\tQ\\t=\\t[%s]\\n' - 1, join[string[Q - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tsnr\\t=\\t[%s]\\n' - 1, join[string[snr - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tP\\t=\\t%d\\n' - 1, P - 1]
fprintf[1 - 1, '\\tNr\\t=\\t%d\\n' - 1, Nr - 1]
fprintf[1 - 1, '\\tN_ratio\\t=\\t%d\\n' - 1, N_ratio - 1]
fprintf[1 - 1, 'Start simulation at %s\\n' - 1, string[datetime['now' - 1] - 1] - 1]
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]

if SHOW_PROGRESS == 1:
    PB = ProgressBar_cli_parfor[Mc - 1]
tic

for i_Mc in np.arange(1, Mc + 1):
    stream = prngsc['Value']
    stream['Substream' - 1] = i_Mc
    RandStream['setGlobalStream'][stream - 1]
    path_full_name = sprintf['%s_mse_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
    r_path_full = fullfile[dir_dump - 1, path_full_name - 1]
    path_full_name = sprintf['%s_est_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
    s_path_full = fullfile[dir_save - 1, path_full_name - 1]
    
    if sim_mode >= 2:
        
        if isfile[r_path_full - 1]:
            r_data = load[r_path_full - 1]
            est_MSE_dfo = r_data['est_MSE_dfo']
            est_MSE_aoa = r_data['est_MSE_aoa']
            est_MSE_chl = r_data['est_MSE_chl']
            s_data = load[s_path_full - 1]
            est_dfoVal = s_data['est_dfoVal']
            est_aoaVal = s_data['est_aoaVal']
            est_chlVal = s_data['est_chlVal']
            l_Q['unmatched_Q'] = intersects[Q - 1, r_data['Q'] - 1]
            l_snr['unmatched_snr'] = intersects[snr - 1, r_data['snr'] - 1]
            f_Q_idx = arrcmp[l_Q - 1, Q - 1, 1 - 1]
            f_snr_idx = arrcmp[l_snr - 1, snr - 1, 1 - 1]
            
            if unmatched_snr or unmatched_Q:
                l_Q_idx = arrcmp[l_Q - 1, r_data['Q'] - 1, 1 - 1]
                l_snr_idx = arrcmp[l_snr - 1, r_data['snr'] - 1, 1 - 1]
                fill_r_data = np.zeros((n_Q, n_snr))
                fill_s_data = cell[n_Q - 1, n_snr - 1]
                fill_r_data(f_Q_idx, f_snr_idx) = est_MSE_dfo[l_Q_idx - 1, l_snr_idx - 1]
                fill_s_data(f_Q_idx, f_snr_idx) = est_dfoVal[l_Q_idx - 1, l_snr_idx - 1]
                r_MSE_dfo_Mc(:, :, i_Mc) = fill_r_data
                s_est_dfo_Mc(:, :, i_Mc) = fill_s_data
                fill_r_data = np.zeros((n_Q, n_snr))
                fill_s_data = cell[n_Q - 1, n_snr - 1]
                fill_r_data(f_Q_idx, f_snr_idx) = est_MSE_aoa[l_Q_idx - 1, l_snr_idx - 1]
                fill_s_data(f_Q_idx, f_snr_idx) = est_aoaVal[l_Q_idx - 1, l_snr_idx - 1]
                r_MSE_aoa_Mc(:, :, i_Mc) = fill_r_data
                s_est_aoa_Mc(:, :, i_Mc) = fill_s_data
                fill_r_data = np.zeros((n_Q, n_snr))
                fill_s_data = cell[n_Q - 1, n_snr - 1]
                fill_r_data(f_Q_idx, f_snr_idx) = est_MSE_chl[l_Q_idx - 1, l_snr_idx - 1]
                fill_s_data(f_Q_idx, f_snr_idx) = est_chlVal[l_Q_idx - 1, l_snr_idx - 1]
                r_MSE_chl_Mc(:, :, i_Mc) = fill_r_data
                s_est_chl_Mc(:, :, i_Mc) = fill_s_data
            else:
                r_MSE_dfo_Mc(:, :, i_Mc) = est_MSE_dfo
                r_MSE_aoa_Mc(:, :, i_Mc) = est_MSE_aoa
                r_MSE_chl_Mc(:, :, i_Mc) = est_MSE_chl
                s_est_dfo_Mc(:, :, i_Mc) = est_dfoVal
                s_est_aoa_Mc(:, :, i_Mc) = est_aoaVal
                s_est_chl_Mc(:, :, i_Mc) = est_chlVal
            valid_Q_Mc(:, i_Mc) = full[sparse[f_Q_idx - 1, np.ones((length[f_Q_idx - 1], 1)) - 1, 1 - 1, n_Q - 1, 1 - 1] - 1]
            valid_snr_Mc(:, i_Mc) = full[sparse[f_snr_idx - 1, np.ones((length[f_snr_idx - 1], 1)) - 1, 1 - 1, n_snr - 1, 1 - 1] - 1]
    elif (sim_mode >= 1 and isfile[r_path_full - 1]) and isfile[s_path_full - 1]:
        r_data = load[r_path_full - 1]
        s_data = load[s_path_full - 1]
        l_Q['r_unmatched_Q'] = intersects[Q - 1, r_data['Q'] - 1]
        l_snr['r_unmatched_snr'] = intersects[snr - 1, r_data['snr'] - 1]
        l_Q['s_unmatched_Q'] = intersects[l_Q - 1, s_data['Q'] - 1]
        l_snr['s_unmatched_snr'] = intersects[l_snr - 1, s_data['snr'] - 1]
        
        if ((r_unmatched_snr or s_unmatched_snr) or r_unmatched_Q) or s_unmatched_Q:
            l_Q_idx = arrcmp[l_Q - 1, r_data['Q'] - 1, 1 - 1]
            l_snr_idx = arrcmp[l_snr - 1, r_data['snr'] - 1, 1 - 1]
            est_MSE_dfo['est_MSE_aoa']['est_MSE_chl']['est_dfoVal']['est_aoaVal']['est_chlVal'] = one_Mc_est[i_Mc - 1, psimset['Value'] - 1, l_Q - 1, l_snr - 1]
            f_Q_idx = arrcmp[l_Q - 1, Q - 1, 1 - 1]
            f_snr_idx = arrcmp[l_snr - 1, snr - 1, 1 - 1]
            est_MSE_dfo(f_Q_idx, f_snr_idx) = r_data['est_MSE_dfo'][l_Q_idx - 1, l_snr_idx - 1]
            est_MSE_aoa(f_Q_idx, f_snr_idx) = r_data['est_MSE_aoa'][l_Q_idx - 1, l_snr_idx - 1]
            est_MSE_chl(f_Q_idx, f_snr_idx) = r_data['est_MSE_chl'][l_Q_idx - 1, l_snr_idx - 1]
            s_data = load[s_path_full - 1]
            est_dfoVal(f_Q_idx, f_snr_idx) = s_data['est_dfoVal'][l_Q_idx - 1, l_snr_idx - 1]
            est_aoaVal(f_Q_idx, f_snr_idx) = s_data['est_aoaVal'][l_Q_idx - 1, l_snr_idx - 1]
            est_chlVal(f_Q_idx, f_snr_idx) = s_data['est_chlVal'][l_Q_idx - 1, l_snr_idx - 1]
            r_MSE_dfo_Mc(:, :, i_Mc) = est_MSE_dfo
            r_MSE_aoa_Mc(:, :, i_Mc) = est_MSE_aoa
            r_MSE_chl_Mc(:, :, i_Mc) = est_MSE_chl
            s_est_dfo_Mc(:, :, i_Mc) = est_dfoVal
            s_est_aoa_Mc(:, :, i_Mc) = est_aoaVal
            s_est_chl_Mc(:, :, i_Mc) = est_chlVal
            dump_name = sprintf['%s_est_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
            r_path_full = fullfile[dir_save - 1, dump_name - 1]
            parsave[r_path_full - 1, est_dfoVal - 1, est_aoaVal - 1, est_chlVal - 1, Q - 1, snr - 1, P - 1, Nr - 1]
            dump_name = sprintf['%s_mse_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
            r_path_full = fullfile[dir_dump - 1, dump_name - 1]
            parsave[r_path_full - 1, est_MSE_dfo - 1, est_MSE_aoa - 1, est_MSE_chl - 1, Q - 1, snr - 1, P - 1, Nr - 1]
        else:
            r_MSE_dfo_Mc(:, :, i_Mc) = r_data['est_MSE_dfo']
            r_MSE_aoa_Mc(:, :, i_Mc) = r_data['est_MSE_aoa']
            r_MSE_chl_Mc(:, :, i_Mc) = r_data['est_MSE_chl']
            s_est_dfo_Mc(:, :, i_Mc) = s_data['est_dfoVal']
            s_est_aoa_Mc(:, :, i_Mc) = s_data['est_aoaVal']
            s_est_chl_Mc(:, :, i_Mc) = s_data['est_chlVal']
        valid_Q_Mc(:, i_Mc) = 1
        valid_snr_Mc(:, i_Mc) = 1
    else:
        est_MSE_dfo['est_MSE_aoa']['est_MSE_chl']['est_dfoVal']['est_aoaVal']['est_chlVal'] = one_Mc_est[i_Mc - 1, psimset['Value'] - 1]
        r_MSE_dfo_Mc(:, :, i_Mc) = est_MSE_dfo
        r_MSE_aoa_Mc(:, :, i_Mc) = est_MSE_aoa
        r_MSE_chl_Mc(:, :, i_Mc) = est_MSE_chl
        s_est_dfo_Mc(:, :, i_Mc) = est_dfoVal
        s_est_aoa_Mc(:, :, i_Mc) = est_aoaVal
        s_est_chl_Mc(:, :, i_Mc) = est_chlVal
        valid_Q_Mc(:, i_Mc) = 1
        valid_snr_Mc(:, i_Mc) = 1
        dump_name = sprintf['%s_est_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
        r_path_full = fullfile[dir_save - 1, dump_name - 1]
        parsave[r_path_full - 1, est_dfoVal - 1, est_aoaVal - 1, est_chlVal - 1, Q - 1, snr - 1, P - 1, Nr - 1]
        dump_name = sprintf['%s_mse_%03d.est.mat' - 1, sim_name - 1, i_Mc - 1]
        r_path_full = fullfile[dir_dump - 1, dump_name - 1]
        parsave[r_path_full - 1, est_MSE_dfo - 1, est_MSE_aoa - 1, est_MSE_chl - 1, Q - 1, snr - 1, P - 1, Nr - 1]
    
    if SHOW_PROGRESS == 1:
        advance[PB - 1]
fprintf[1 - 1, 'done!\\n' - 1]
sim_exe_time = toc
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]
fprintf[1 - 1, 'Simulation ends at %s\\n' - 1, string[datetime['now' - 1] - 1] - 1]
fprintf[1 - 1, 'Execution time: %s\\n' - 1, show_duration[sim_exe_time - 1] - 1]
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]
count_Mc = np.zeros((n_Q, n_snr))

for i_Mc in np.arange(1, Mc + 1):
    count_Mc = count_Mc + valid_Q_Mc[: - 1, i_Mc - 1] @ valid_snr_Mc[: - 1, i_Mc - 1].T
uni_count_Mc = unique[count_Mc - 1]
uni_count_Mc(uni_count_Mc == 0) = None

if length[uni_count_Mc - 1] != 1:
    warning['Unequal number of simulation runs!' - 1]
Mc = max[uni_count_Mc - 1, None - 1, 'all' - 1]
MSE_dfo = squeeze[sum[r_MSE_dfo_Mc - 1, 3 - 1] / count_Mc - 1]
MSE_aoa = squeeze[sum[r_MSE_aoa_Mc - 1, 3 - 1] / count_Mc - 1]
MSE_chl = squeeze[sum[r_MSE_chl_Mc - 1, 3 - 1] / count_Mc - 1]
fprintf[1 - 1, 'Collecting data... (valid Mc = %d)\\n' - 1, Mc - 1]
save_name = sprintf['%s_channel_config.est.mat' - 1, sim_name - 1]
r_path_full = fullfile[dir_save - 1, save_name - 1]
save[r_path_full - 1, 'config' - 1]
save_name = sprintf['%s_sim_config.est.mat' - 1, sim_name - 1]
r_path_full = fullfile[dir_save - 1, save_name - 1]
save[r_path_full - 1, 'Mc' - 1, 'Q' - 1, 'snr' - 1, 'P' - 1, 'Nr' - 1, 'N_ratio' - 1]
dir_result = fullfile['results' - 1, dir_sim - 1]

if not exist[dir_result - 1, 'dir' - 1]:
    mkdir[dir_result - 1]
result_name = sprintf['%s_channel_config.est.mat' - 1, sim_name - 1]
r_path_full = fullfile[dir_result - 1, result_name - 1]
save[r_path_full - 1, 'config' - 1]
result_name = sprintf['%s_sim_config.est.mat' - 1, sim_name - 1]
r_path_full = fullfile[dir_result - 1, result_name - 1]
save[r_path_full - 1, 'Mc' - 1, 'Q' - 1, 'snr' - 1, 'P' - 1, 'Nr' - 1, 'N_ratio' - 1, 'sim_exe_time' - 1]
result_name = sprintf['%s_mse_dfo_aoa_channel.est.mat' - 1, sim_name - 1]
r_path_full = fullfile[dir_result - 1, result_name - 1]
save[r_path_full - 1, 'MSE_dfo' - 1, 'MSE_aoa' - 1, 'MSE_chl' - 1]