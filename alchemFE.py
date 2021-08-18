import numpy as np
import matplotlib.pyplot as plt
import pymbar
import os
#import alchemlyb

import parse_FE_AMBER
import FE_TI
import calculate_MBAR
import FE_MBAR

# Temperature of simulations
Temp = 300

# Give directory containing subdirectories for all windows
dir_simulations = '../simulations'

# Parse dVdl time series from .out files
print("Parsing dV/dl...")
list_of_dirs = [x.path for x in os.scandir(path='../simulations') if x.is_dir()]
list_of_dirs.sort()
windows = [float(list_of_dirs[i].split('/')[2]) for i in range(len(list_of_dirs))]
dVdls = [parse_FE_AMBER.parse_TI(subdir) for subdir in list_of_dirs] # Parse data from .out files    

print("Calculating DeltaG from TI...")
#dVdls = [dVdl[pymbar.timeseries.subsampleCorrelatedData(dVdl)] for dVdl in dVdls] # Subsample uncorrelated data in case of correlations
fe_ti = FE_TI.ti(dVdls, windows) # Calculate results from TI using numerical integration and error propagation
fe_ti.plot_time_series()
fe_ti.plot_trapz()
[av_ti, s_ti] = fe_ti.results()
print(f'DeltaG = {av_ti} pm {s_ti}')

# Parse u_nk time series from .out files
print("Parsing MBAR Energies...")
u_kns = [parse_FE_AMBER.parse_MBAR(subdir) for subdir in list_of_dirs] # Parse data from .out files
print("Calculating DeltaG from MBAR...")
data_mbar = FE_MBAR.fe_mbar(u_kns, windows, Temp)
[av_mbar, s_mbar] = data_mbar.get_freeEnergy()

print(av_mbar, s_mbar)