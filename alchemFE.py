import numpy as np
import matplotlib.pyplot as plt
import pymbar
import os
#import alchemlyb

import parse_FE_AMBER
import FE_TI
import calculate_MBAR
import FE_MBAR

# Give directory containing subdirectories for all windows
dir_simulations = '../simulations'

# Parse dVdl time series from .out files
print("Parsing DV/DL...")
list_of_dirs = [x.path for x in os.scandir(path='../simulations') if x.is_dir()]
list_of_dirs.sort()
windows = [float(list_of_dirs[i].split('/')[2]) for i in range(len(list_of_dirs))]
dVdls = [parse_FE_AMBER.parse_TI(subdir) for subdir in list_of_dirs] # Parse data from .out files    

#dVdls = [dVdl[pymbar.timeseries.subsampleCorrelatedData(dVdl)] for dVdl in dVdls] # Subsample uncorrelated data in case of correlations
fe_ti = FE_TI.ti(dVdls, windows) # Calculate results from TI using numerical integration and error propagation
fe_ti.plot_time_series()
#fe_ti.plot_trapz()
[av_ti, s_ti] = fe_ti.results()
print(f'DeltaG = {av_ti} pm {s_ti}')

# Parse u_nk time series from .out files
print("Parsing MBAR Energies...")
u_kns = [parse_FE_AMBER.parse_MBAR(subdir) for subdir in list_of_dirs] # Parse data from .out files
u_kn = np.concatenate(u_kns,1)
print(u_kn.shape)
N_k = [1250]*5 + [1249] + [1250]*13 + [1249] + [1246]*2 + [1240, 1232, 1237, 1237, 1224, 1235, 1236]
print("Calculating DeltaG...")
results_mbar = pymbar.MBAR(u_kn, N_k, maximum_iterations=10000)
DeltaGs = results_mbar.getFreeEnergyDifferences()['Delta_f']
print(DeltaGs)
#u_kns = [u_kns[]] # Subsample uncorrelated data in case of correlations
fe_mbar = calculate_MBAR.get_FE(u_kns) # Calculate results from MBAR using pymbar
#fe_mbar.plot_overlap()
[av_mbar, s_mbar] = fe_mbar.results()
print(av_mbar, s_mbar)