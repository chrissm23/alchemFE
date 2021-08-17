import numpy as np
import matplotlib.pyplot as plt
import pymbar
import os
#import alchemlyb

import parse_FE_AMBER
import calculate_TI
import FE_TI
import calculate_MBAR
import FE_MBAR

# Give directory containing subdirectories for all windows
dir_simulations = '../simulations'

# Parse dVdl time series from .out files
for root, subdirs, files in os.walk(dir_simulations):
    dVdls = [parse_FE_AMBER.parse_TI(os.path.join(root, subdir)) for subdir in subdirs] # Parse data from .out files

#dVdls = [dVdl[pymbar.timeseries.subsampleCorrelatedData(dVdl)] for dVdl in dVdls] # Subsample uncorrelated data in case of correlations
dVdl_concatenated = np.concatenate(dVdls)
plt.plot(dVdl_concatenated)
plt.show()
fe_ti = calculate_TI.get_FE(dVdls) # Calculate results from TI using numerical integration and error propagation
fe_ti.plot()
[av_ti, s_ti] = fe_ti.results()
print(av_ti, s_ti)

# Parse u_nk time series from .out files
for root, subdirs, files in os.walk(dir_simulations):
    u_kns = [parse_FE_AMBER.parse_MBAR(os.path.join(root, subdir)) for subdir in subdirs] # Parse data from .out files

#u_kns = [u_kns[]] # Subsample uncorrelated data in case of correlations
fe_mbar = calculate_MBAR.get_FE(u_kns) # Calculate results from MBAR using pymbar
fe_mbar.plot_overlap()
[av_mbar, s_mbar] = fe_mbar.results()
print(av_mbar, s_mbar)