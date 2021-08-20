import numpy as np
import matplotlib.pyplot as plt
import pymbar
import os
from scipy.constants import k as k_B

def parse_TI(dir_path):
    """Parse dV/DL values from .out file"""
    file_path = dir_path + '/ti001.out' # Path to file
    dvdl = []

    # Read file and separate results
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.split('=')[0].strip() == 'DV/DL':
                dvdl.append(line.split('=')[1].strip())
            if line.strip() == 'A V E R A G E S   O V E R    1250 S T E P S':
                break
    
    dvdl = [float(dvdl[i]) for i in range(len(dvdl)) if i%2 == 0]
    dvdl_np = np.array(dvdl)
    #plt.plot(dvdl_np)
    #plt.show()
    return dvdl_np

def parse_MBAR(dir_path):
    """Parse MBAR values from .out file"""
    file_path = dir_path + '/ti001.out' # Path to file
    u_kn = []

    # Read file and separate results
    with open(file_path, 'r') as f:
        lines = f.readlines()
        mbar_section = False # Flag to indicate MBAR energies reached
        u_n = []
        for line in lines:
            if (line.strip() == '------------------------------------------------------------------------------') and (mbar_section == True):
                mbar_section = False
                u_kn.append(u_n)
                u_n = []
            if mbar_section == True:
                if line.split('=')[1].strip() == '****************':
                    u_n.append(np.NaN)
                elif float(line.split('=')[1].strip()) > 0:
                    u_n.append(np.NaN)
                else:
                    u_n.append(float(line.split('=')[1].strip()))
            if line.strip() == 'MBAR Energy analysis:':
                mbar_section = True

    u_kn_np = np.asarray(u_kn)
    return u_kn_np.T


if __name__ == '__main__':
    dvdl_np = parse_MBAR('../simulations/0.00')
    print(dvdl_np.shape)