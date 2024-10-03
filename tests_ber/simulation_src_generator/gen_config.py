import numpy as np
config = struct
config['N' - 1] = 1024
config['Lcp' - 1] = 64
config['beta' - 1] = 0.5
config['fc' - 1] = 6000000000.0
config['fs' - 1] = 10000000.0
config['mod_type' - 1] = 'QPSK'
config['SP' - 1] = 0.5
config['LOS' - 1] = 0
config['v' - 1] = 300
config['DS' - 1] = 1e-06
config['pg_low' - 1] = -20
config['pg_high' - 1] = 0
config['Lch' - 1] = 23
config['dfo_gap' - 1] = 0.046
config['aoa_gap' - 1] = 0.02
config['H' - 1] = 5
config['data_block' - 1] = 5
destdirectory = '_config'

if not exist[destdirectory - 1, 'dir' - 1]:
    mkdir[destdirectory - 1]
fulldestination = fullfile[destdirectory - 1, 'default_config.mat' - 1]
save[fulldestination - 1, 'config' - 1]
print('=====> config saved')