import numpy as np
import matplotlib.pyplot as plt
from numpy.core.numeric import indices
from numpy.lib.function_base import median
from scipy.constants import k as k_B
from scipy.constants import N_A
import os

class fe_mbar:
    """Class for methods and results of MBAR"""
    def __init__(self, u_kns, windows, Temp) -> None:
        self.u_kns = u_kns
        self.windows = windows
        self.Temp = Temp
        self.dfe = None
        self.ddfe = None
        self.Eav = None
        self.Evar = None
        self.overlap = None
        self.beta = None
        self.u_kns_nonan_np = None
        self.u_kns_renorm = None
        self.u_kns_renorm_dimless = None
        self.N_k = []

        self.get_inverseTemp(Temp)
    
    def get_inverseTemp(self, Temp):
        """Calculate inverse temperature in kcal/mol"""
        self.beta = k_B*Temp*N_A/4184

    def del_NaNs(self):
        """Return u_kns_noNaN with no NaN values and N_k list with size of positions for each samplig state"""
        u_kns_nonan = []
        for u_n in self.u_kns:
            index_list_nan = np.argwhere(np.isnan(u_n)) # Get array of indices of NaN values
            # Get list of frames with MBAR NaN values
            list_of_positions = []
            for index_nan in index_list_nan:
                if not index_nan[1] in list_of_positions:
                    list_of_positions.append(index_nan[1])
            u_n_nonan = np.delete(u_n, obj=list_of_positions, axis=1) # Delete NaN values
            u_kns_nonan.append(u_n_nonan)
            self.N_k.append(u_n_nonan.shape[1])
        self.u_kns_nonan_np = np.concatenate(u_kns_nonan, axis=1)

    def get_freeEnergy(self):
        """Use pymbar to get free energy differences and their uncertainties"""
        self.del_NaNs()
        medians = np.median(self.u_kns_nonan_np, axis=1)
        stds = np.std(self.u_kns_nonan_np, axis=1)
        median_of_medians = np.median(medians+stds)
        print(median_of_medians)