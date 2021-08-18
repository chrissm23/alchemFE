import numpy as np
import matplotlib.pyplot as plt
import os

class ti:
    """Class for methods and results of TI"""
    def __init__(self, dVdls, windows) -> None:
        self.dVdls = dVdls
        self.windows = windows
        self.avs = None
        self.vars = None
        self.Eav = None
        self.Evar = None

        self.get_avs_n_vars(self.dVdls)
    
    def get_avs_n_vars(self, dVdls):
        """Function to get average gradients and their variances for numerical integration and error propagation"""
        self.avs = [dVdl.mean() for dVdl in dVdls]
        self.vars = [dVdl.var() for dVdl in dVdls]

    def plot_time_series(self):
        """Function to get plot of time series of dVdl"""
        dVdls_concatenated = np.concatenate(self.dVdls)
        fig_tseries, ax_tseries = plt.subplots()
        ax_tseries.plot(dVdls_concatenated)
        fig_tseries.savefig('TI_dVdl.pdf')

    def results(self):
        """Calculate numerical integration and error propagation"""
        windows_np = np.asarray(self.windows)
        avs_np = np.asarray(self.avs)
        vars_np = np.asarray(self.vars)
        dlambda = np.diff(windows_np)
        areas = np.array([(avs_np[k] + avs_np[k+1])*dlambda[k]/2 for k in range(avs_np.shape[0]-1)])
        self.Eav = areas.sum()
        error0 = self.vars[0]*np.power(dlambda[0],2)/4
        errorN = self.vars[-1]*np.power(dlambda[-1],2)/4
        error = [self.vars[k]*np.power(dlambda[k-1]+dlambda[k],2)/4 for k in range(1,vars_np.shape[0]-1)]
        error = error0 + error + errorN
        error_np = np.asarray(error)
        self.Evar = error_np.sum()
        return [self.Eav, np.sqrt(self.Evar)]

    def plot_trapz(self):
        """Plot numerical integration curve"""
        windows_np = np.asarray(self.windows)
        avs_np = np.asarray(self.avs)
        vars_np = np.asarray(self.vars)
        fig_trapz, ax_trapz = plt.subplots()
        ax_trapz.errorbar(windows_np, avs_np, yerr=np.sqrt(vars_np), color='red', ls='--', marker='o', capsize=5, capthick=1, ecolor='black')
        ax_trapz.fill_between(windows_np, avs_np, y2=0)
        fig_trapz.savefig('TI_trapz.pdf')