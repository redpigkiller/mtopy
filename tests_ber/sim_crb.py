import numpy as np
clc
clear
close
SHOW_PROGRESS = 1
SEED = 506
addpath[genpath['src' - 1] - 1]
default_sim_Mc = 5000
default_sim_snr = np.arange(-10, 40 + 10, 10)
default_sim_Q = np.arange(1, 4 + 1)
default_sim_P = 4
default_sim_Nr = 1
default_exp_name = 'first try'
answer['IsCancelled'] = request_user_input_sim_crb[default_sim_Mc - 1, default_exp_name - 1]

if IsCancelled:
    
    return
sim_name = answer['sim_src_name']
default_sim_Mc = answer['Mc']
sub_trial = answer['exp_name']
dir_sim = fullfile[sim_name - 1, sub_trial - 1]
flag_use_parfor = answer['flag_use_parfor']
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
P = default_sim_P
Nr = default_sim_Nr
n_snr = length[snr - 1]
n_Q = length[Q - 1]
sim_Mc_info = struct
sim_Mc_info['snr' - 1] = snr
sim_Mc_info['Q' - 1] = Q
sim_Mc_info['P' - 1] = P
sim_Mc_info['Nr' - 1] = Nr
sim_Mc_info['config' - 1] = config
sim_Mc_info['dir_gendata' - 1] = fullfile['_gendata' - 1, sim_name - 1, sim_name - 1]
sim_Mc_info['snr_idx' - 1] = snr_idx
sim_Mc_info['Q_idx' - 1] = Q_idx
r_dfo_crb_Mc = np.zeros((n_Q, n_snr, Mc))
r_aoa_crb_Mc = np.zeros((n_Q, n_snr, Mc))

if flag_use_parfor != 0:
    poolobj = startparpool[]
    parforArg = poolobj['NumWorkers']
else:
    parforArg = 0
parfevalOnAll[warning - 1, 0 - 1, 'off' - 1, 'all' - 1]
prngsc = parallel['pool']['Constant'][RandStream['Threefry' - 1, 'Seed' - 1, SEED - 1] - 1]
psimset = parallel['pool']['Constant'][sim_Mc_info - 1]
fprintf[1 - 1, 'Simulation info:\\n' - 1]
fprintf[1 - 1, '\\tsim_src:\\t%s\\n' - 1, sim_name - 1]
fprintf[1 - 1, '\\texp_name:\\t%s\\n' - 1, sub_trial - 1]
fprintf[1 - 1, '\\tMc\\t=\\t%d\\n' - 1, Mc - 1]
fprintf[1 - 1, '\\tQ\\t=\\t[%s]\\n' - 1, join[string[Q - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tsnr\\t=\\t[%s]\\n' - 1, join[string[snr - 1] - 1, ',' - 1] - 1]
fprintf[1 - 1, '\\tP\\t=\\t%d\\n' - 1, P - 1]
fprintf[1 - 1, '\\tNr\\t=\\t%d\\n' - 1, Nr - 1]
fprintf[1 - 1, 'Start simulation at %s\\n' - 1, string[datetime['now' - 1] - 1] - 1]
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]

if SHOW_PROGRESS == 1:
    PB = ProgressBar_cli_parfor[Mc - 1]
tic

for i_Mc in np.arange(1, Mc + 1):
    r_dfo_crb['r_aoa_crb'] = one_Mc_crb[i_Mc - 1, psimset['Value'] - 1]
    r_dfo_crb_Mc(:, :, i_Mc) = r_dfo_crb
    r_aoa_crb_Mc(:, :, i_Mc) = r_aoa_crb
    
    if SHOW_PROGRESS == 1:
        advance[PB - 1]
fprintf[1 - 1, 'done!\\n' - 1]
sim_exe_time = toc
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]
fprintf[1 - 1, 'Simulation ends at %s\\n' - 1, string[datetime['now' - 1] - 1] - 1]
fprintf[1 - 1, 'Execution time: %s\\n' - 1, show_duration[sim_exe_time - 1] - 1]
fprintf[1 - 1, '--------------------------------------------------\\n' - 1]
avg_dfo_crb = squeeze[sum[r_dfo_crb_Mc - 1, 3 - 1] / Mc - 1]
avg_aoa_crb = squeeze[sum[r_aoa_crb_Mc - 1, 3 - 1] / Mc - 1]
dir_result = fullfile['results_crb' - 1, dir_sim - 1]

if not exist[dir_result - 1, 'dir' - 1]:
    mkdir[dir_result - 1]
path_full_name = sprintf['%s_channel_config.crb.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'config' - 1]
path_full_name = sprintf['%s_sim_config.crb.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'Mc' - 1, 'Q' - 1, 'snr' - 1, 'P' - 1, 'Nr' - 1, 'sim_exe_time' - 1]
path_full_name = sprintf['%s_avg_crb.crb.mat' - 1, sim_name - 1]
path_full = fullfile[dir_result - 1, path_full_name - 1]
save[path_full - 1, 'avg_dfo_crb' - 1, 'avg_aoa_crb' - 1]