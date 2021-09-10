'''
Created on Apr 24, 2021

@author: Jimmy Palomino
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def StatorMaterial():
    """This function adds the stator material

    Args:
        main (Dic): Main dictionary used to upload the information

    Returns:
        Dic: Same unmodified main dictionary.
    """

    
    H, B = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialBHCurve.csv',
                      skiprows=5, unpack=True, delimiter=',')

    # B-H Curve Interpolation----------------------------------------------------------------
    # Transforming en kA/m
    H = H/1000

    # Redefining useful range
    # Here considerer as maximum a slop of 10 degrees
    BHslop = (B[1:]-B[:-1])/((H[1:]-H[:-1]))-np.tan(np.pi*2.5/180)

    HUseful = H[:-1][BHslop > 0.]
    BUseful = B[:-1][BHslop > 0.]

    # Interpolation using cubic spline
    p = interp1d(HUseful, BUseful, kind='cubic')
    p2 = interp1d(BUseful, HUseful, kind='cubic')

    # Supersamplig the BH curve
    Hnew = np.linspace(min(HUseful), max(HUseful), 10000)
    Bnew = p(Hnew)

    # Knee point finding
    slop = (Bnew[1:]-Bnew[:-1])/((Hnew[1:]-Hnew[:-1]))-np.tan(45/180*np.pi)
    HKnee = np.mean(Hnew[:-1][np.abs(slop) < 0.01])

    return p2
