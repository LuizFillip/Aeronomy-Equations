import numpy as np

def scale_gradient(Ne, dz = 1):
    """length scale gradiendt : Vertical variation of density"""
    factor = 1e-3 #convert km to meters
    return np.gradient(np.log(Ne), dz)*factor