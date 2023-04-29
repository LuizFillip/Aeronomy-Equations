import numpy as np

def scale_gradient(Ne, dz = 1, factor = 1e-3):
    """
    length scale gradient: Vertical variation of density
    
    Parameters:
        factor: convert km to meters
    """
    return np.gradient(np.log(Ne), dz)*factor