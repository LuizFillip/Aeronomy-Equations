import numpy as np

def scale_gradient(Ne, dz = 1, factor = 1e-3):
    """
    length scale gradient: Vertical variation of density
    
    Parameters:
        factor: convert km to meters
    """
    return np.gradient(np.log(Ne), dz, edge_order = 2)*factor



def vz_out_equator(vz, uy, wd, i):
    """
    A general expression for vertical plasma drift including
    the effect from meridional wind and plasma diffusion
    """
    I = np.radians(i)
    
    vz_term = vz * np.cos(I)
    uy_term = uy * np.cos(I) * np.sin(I)
    wd_term = wd * pow(np.sin(I), 2)
    
    return vz_term + uy_term - wd_term 
