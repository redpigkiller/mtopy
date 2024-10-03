import numpy as np
cmap = np.array([['b', 'k', 'r', '#3E9651', '#7E2F8E', '#D95319', '#4DBEEE']])
makr = np.array([['*', 'diamond', 'o', 'square', 'x', '^']])
lins = np.array([['-', '--', ':', '-.']])
addpath[genpath['src' - 1] - 1]
answer['IsCancelled'] = request_user_input1()

if IsCancelled == 1:
    
    return
sim_src = (answer, 'sim_src')[1 - 1]
sim_exp = answer['sim_exp']
plot_metric = answer['dataMetric']
name_answer['IsCancelled'] = request_user_input2(sim_exp)
plot_Q = name_answer['plot_Q']
est_data_name = sprintf['%s_mse_dfo_aoa_channel.est.mat' - 1, sim_src - 1]
ber_data_name = sprintf['%s_avg_ber.ber.mat' - 1, sim_src - 1]
est_config_name = sprintf['%s_channel_config.est.mat' - 1, sim_src - 1]
est_sim_config_name = sprintf['%s_sim_config.est.mat' - 1, sim_src - 1]
ber_config_name = sprintf['%s_channel_config.ber.mat' - 1, sim_src - 1]
ber_sim_config_name = sprintf['%s_sim_config.ber.mat' - 1, sim_src - 1]
dir_fig = fullfile['figure' - 1, 'comparison' - 1]

if not exist[dir_fig - 1, 'dir' - 1]:
    mkdir[dir_fig - 1]
n_exp = length[sim_exp - 1]
sim_exp_name = cell[n_exp - 1, 1 - 1]
data = cell[n_exp - 1, 1 - 1]
config = cell[n_exp - 1, 1 - 1]
sim_config = cell[n_exp - 1, 1 - 1]

for i_exp in np.arange(1, n_exp + 1):
    (sim_exp_name, i_exp)[] = getfield[name_answer - 1, sprintf['sim_exp_name_%d' - 1, i_exp - 1] - 1]
    
    if true == (strcmpi[plot_metric - 1, 'MSE DFO' - 1] == 1):
        dir_sim = fullfile[sim_src - 1, sim_exp[i_exp - 1] - 1]
        (data, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_data_name - 1] - 1]['MSE_dfo']
        (config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_config_name - 1] - 1]['config']
        (sim_config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_sim_config_name - 1] - 1]
    elif true == (strcmpi[plot_metric - 1, 'MSE AOA' - 1] == 1):
        dir_sim = fullfile[sim_src - 1, sim_exp[i_exp - 1] - 1]
        (data, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_data_name - 1] - 1]['MSE_aoa']
        (config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_config_name - 1] - 1]['config']
        (sim_config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_sim_config_name - 1] - 1]
    elif true == (strcmpi[plot_metric - 1, 'MSE Channel' - 1] == 1):
        dir_sim = fullfile[sim_src - 1, sim_exp[i_exp - 1] - 1]
        (data, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_data_name - 1] - 1]['MSE_chl']
        (config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_config_name - 1] - 1]['config']
        (sim_config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, est_sim_config_name - 1] - 1]
    elif true == (strcmpi[plot_metric - 1, 'BER' - 1] == 1):
        dir_sim = fullfile[sim_src - 1, sim_exp[i_exp - 1] - 1]
        (data, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, ber_data_name - 1] - 1]['avg_ber']
        (config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, ber_config_name - 1] - 1]['config']
        (sim_config, i_exp)[] = load[fullfile['results' - 1, dir_sim - 1, ber_sim_config_name - 1] - 1]
    else:
        pass
fig = figure[1 - 1]

for i_exp in np.arange(1, n_exp + 1):
    Q = (((sim_config, i_exp),),)['Q']
    snr = (((sim_config, i_exp),),)['snr']
    
    for i_Q in np.arange(length[Q - 1], 1 + -1, -1):
        
        if not ismember[Q[i_Q - 1] - 1, plot_Q - 1]:
            
            continue
        semilogy[snr - 1, data[i_exp - 1][i_Q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([[(((sim_exp_name, i_exp),),), ' (Q=', str(Q[i_Q - 1]), ')']]) - 1, 'Color' - 1, cmap[i_Q - 1] - 1, 'Marker' - 1, makr[i_Q - 1] - 1, 'LineStyle' - 1, lins[i_exp - 1] - 1, 'LineWidth' - 1, 1 - 1]
        hold['' - 1]
hold['f' - 1]
xlabel['snr' - 1]
ylabel[plot_metric - 1]
grid['' - 1]
title_str = 'comparison'
title[title_str - 1]
lgd = legend['Location' - 1, 'southwest' - 1]
a = annotation['rectangle' - 1, np.array([[0, 0, 1, 1]]) - 1, 'Color' - 1, 'w' - 1]
fname = sprintf['%s_comparison_on_%s' - 1, sim_src - 1, plot_metric - 1]
path_full = fullfile[dir_fig - 1, fname - 1]
saveas[fig - 1, strcat[path_full - 1, '.fig' - 1] - 1]
exportgraphics[fig - 1, strcat[path_full - 1, '.png' - 1] - 1, 'Resolution' - 1, 300 - 1]
delete[a - 1]


def request_user_input1():
    dir_dmp_now = get_subfolders_r['results' - 1, 2 - 1]
    
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
    formats[1 - 1, 1 - 1]['size' - 1] = np.array([[200, 75]])
    formats[1 - 1, 1 - 1]['format' - 1] = 'text'
    formats[1 - 1, 1 - 1]['items' - 1] = dir_now['name']
    formats[1 - 1, 1 - 1]['callback' - 1] = lambda _, _, h, k: set[h[k + 1 - 1] - 1, 'String' - 1, (dir_now, 'array')[get[h[k - 1] - 1, 'Value' - 1] - 1]['name'] - 1, 'Value' - 1, 1 - 1]
    prompt(2, :) = [['Simulation experiment:', 'sim_exp', [[]]]]
    formats[2 - 1, 1 - 1]['type' - 1] = 'list'
    formats[2 - 1, 1 - 1]['style' - 1] = 'listbox'
    formats[2 - 1, 1 - 1]['size' - 1] = np.array([[200, 150]])
    formats[2 - 1, 1 - 1]['format' - 1] = 'text'
    formats[2 - 1, 1 - 1]['items' - 1] = (dir_now, 'array')[1 - 1]['name']
    formats[2 - 1, 1 - 1]['limits' - 1] = np.array([[0, 2]])
    prompt(3, :) = [['Enter data type: ', 'dataMetric', [[]]]]
    formats[3 - 1, 1 - 1]['type' - 1] = 'list'
    formats[3 - 1, 1 - 1]['style' - 1] = 'radiobutton'
    formats[3 - 1, 1 - 1]['size' - 1] = -1
    formats[3 - 1, 1 - 1]['format' - 1] = 'text'
    formats[3 - 1, 1 - 1]['items' - 1] = [['MSE DFO', 'MSE AOA', 'MSE Channel', 'BER']]
    prompt(4, :) = [['Continue to set the plot Q and name of legends...', [[]], [[]]]]
    formats[4 - 1, 1 - 1]['type' - 1] = 'text'
    formats[4 - 1, 1 - 1]['size' - 1] = np.array([[-1, 0]])
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    return answer[IsCancelled]


def request_user_input2(sim_exp):
    n_exp = length[sim_exp - 1]
    prompt = cell[n_exp + 1 - 1, 3 - 1]
    title = 'sim_exp name'
    formats = struct
    defAns = struct
    options = struct
    prompt(1, :) = [['plot Q', 'plot_Q', [[]]]]
    formats[1 - 1, 1 - 1]['type' - 1] = 'edit'
    formats[1 - 1, 1 - 1]['size' - 1] = np.array([[-1, 20]])
    formats[1 - 1, 1 - 1]['format' - 1] = 'vector'
    
    for i_exp in np.arange(1, n_exp + 1):
        data_name = sprintf['sim_exp_name_%d' - 1, i_exp - 1]
        prompt(i_exp + 1, :) = [[sprintf['Input name for %s:' - 1, (((sim_exp, i_exp),),) - 1], data_name, [[]]]]
        formats[i_exp + 1 - 1, 1 - 1]['type' - 1] = 'edit'
        formats[i_exp + 1 - 1, 1 - 1]['size' - 1] = -1
        formats[i_exp + 1 - 1, 1 - 1]['format' - 1] = 'text'
    options['Resize' - 1] = 'off'
    options['AlignControls' - 1] = 'on'
    options['Interpreter' - 1] = 'none'
    options['CancelButton' - 1] = 'off'
    answer['IsCancelled'] = inputsdlg[prompt - 1, title - 1, formats - 1, defAns - 1, options - 1]
    return answer[IsCancelled]