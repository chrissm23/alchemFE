import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import k as k_B
from scipy.constants import N_A
import os
import pymbar

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
        self.u_kns_nonan_np_dimless = None
        self.N_k = []

        self.get_inverseTemp(Temp)
    
    def get_inverseTemp(self, Temp):
        """Calculate inverse temperature in kcal/mol"""
        self.beta = 4184/(k_B*Temp*N_A)

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
        self.u_kns_nonan_np_dimless = self.u_kns_nonan_np*self.beta
        mbar_result = pymbar.MBAR(self.u_kns_nonan_np_dimless, self.N_k)
        results = mbar_result.getFreeEnergyDifferences(return_dict=True, return_theta=True)
        print(results['Delta_f'])
        #print(results['dDelta_f'])
        #print(results['Theta'])

        return results['Delta_f'][0,-1], results['dDelta_f'][0,-1]