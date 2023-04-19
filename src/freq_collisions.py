import numpy as np


def electron_neutral_collision(Tn, Nn, Te, ne):
    """
    The electron-neutral collision rates (frequency) 
    Kelley (2009)
    """
    return (5.4e-10 * Nn * np.sqrt(Tn) + 
            (34 + 4.18 * np.log(Te**3 / ne))
            * ne * Te**(-3/2))

def nui_1(Tn, O, O2, N2):
    """
    The ion-neutral collision frequency
    by Bailey and Balan (1996)
    """
    term_O = (4.45e-11 * O * np.sqrt(Tn) * 
              (1.04 - 0.067 * np.log10(Tn))**2)
    
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2


def nu_3(O, Tn, Ti):
    """
    The ion-neutral collision frequency
    by Schunk and Nagy, 2000

    Parameters
    ----------
    O :  float array
        Molecular oxygen concentration
    Tn : float array
        neutral temperature
    Ti : float array
        ion temperature
    """
    Tr = (Ti + Tn) / 2
    return 3.7e-11 * O * np.sqrt(Tr) * (1 - 0.064 * np.log10(Tr))**2

class collision_frequencies:
    """
    See momentum transfer in Schuck and Nagy 2000
    """
    @staticmethod
    def ion_neutrals(O, O2, N2, T):
        
        CO2 = (2.31e-10 * O + 
              2.59e-11 * O2 * 
              np.sqrt(T) + 4.13e-10 * N2)
                
        CO  = (4.45e-11 * O * np.sqrt(T) + 
              6.64e-10 * O2 + 6.82e-10 * N2)
        
        CN2 = (2.58e-10 * O + 
              4.49e-10 * O2 + 
              5.14e-11 * np.sqrt(T))
                
        CNO = (2.44e-10 *O +
              4.27e-10 * O2 + 
              4.34e-10 * N2)
        
        return (CO2 + CO + CN2 + CNO) / 4.0
    
    @staticmethod
    def electrons_neutrals(O, O2, N2, He, H, Te):
        """Collision frequencies electrons with neutrals """
        #Must substitute T to Te (electron temperature)
        CN2 = 2.33e-11 * N2 * Te
        
        CO2 = 1.82e-10 * O2 * np.sqrt(Te)
        
        CO = 8.90e-11 * O * np.sqrt(Te)
        
        CHe = 4.60e-10 * He * np.sqrt(Te)
        
        CH = 4.50e-09 * H * np.sqrt(Te)
        
        return (CN2 + CO2 + CO + CHe + CH) / 5.0 