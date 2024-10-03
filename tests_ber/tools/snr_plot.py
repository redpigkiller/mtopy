import numpy as np


def snr_plot(id, snr, yval, ylgd, x_text, y_text, t_text, plot_settings):
    
    if nargin < 8:
        is_ylog = 1
        is_grid = 1
        cmap = np.array([['b', 'k', 'r', 'g', 'c', 'm', 'y']])
        makr = np.array([['o', '+', '*', '.', 'x', '-']])
        lins = np.array([['-', '--', ':', '-.']])
        lgd_loc = [['Location', 'southwest']]
    else:
        is_ylog = plot_settings['is_ylog']
        is_grid = plot_settings['is_grid']
        cmap = plot_settings['color']
        makr = plot_settings['marker']
        lins = plot_settings['lines']
        lgd_loc = plot_settings['lgd_loc']
    
    if nargin < 7:
        t_text = sprintf['value of %s' - 1, inputname[3 - 1] - 1]
    
    if nargin < 6:
        y_text = inputname[3 - 1]
    
    if nargin < 5:
        x_text = inputname[2 - 1]
    
    if np.size(yval, 1) != length[ylgd - 1]:
        error['different number of data y' - 1]
    fig = figure[id - 1]
    
    for q in np.arange(1, length[ylgd - 1] + 1):
        
        if is_ylog == 1:
            semilogy[snr - 1, yval[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([[inputname[4 - 1], ' = ', str(ylgd[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
        else:
            plot[snr - 1, yval[q - 1, : - 1] - 1, 'DisplayName' - 1, np.array([[inputname[4 - 1], ' = ', str(ylgd[q - 1])]]) - 1, 'Color' - 1, cmap[q - 1] - 1, 'Marker' - 1, makr[1 - 1] - 1, 'LineStyle' - 1, lins[1 - 1] - 1]
        hold['' - 1]
    hold['f' - 1]
    xlabel[x_text - 1]
    ylabel[y_text - 1]
    title[t_text - 1]
    
    if is_grid == 1:
        grid['' - 1]
    
    if iscell[lgd_loc - 1]:
        legend[lgd_loc[: - 1] - 1]
    return fig