import numpy as np
import scipy.constants as cs


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
    
    


class gyrofrequency:
    
    #default: Equatorial geomagnetic field in Tesla
    @staticmethod
    def ions(B = 0.25e-4):
        """Gyrofrequency for ions in 1/s"""
        effective_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3.
        return cs.elementary_charge * B / effective_mass 
    @staticmethod
    def electrons(B = 0.25e-4):
        """Gyrofrequency for electrons in 1/s"""
        return  cs.elementary_charge * B / cs.electron_mass



def electron_neutral_collision(Tn, Nn):
    """
    The electron-neutral collision rates (frequency) 
    Denadini et al. 2007
    """
    return (5.4e-10) * Nn * np.sqrt(Tn)

def electron_cyclotron(B = 0.285e-04):
    """Electron gyro frequency"""
    return - (cs.elementary_charge * B / cs.electron_mass)

def ion_cyclotron(B = 0.285e-04):
    """Ion gyro frequency"""
    return ( cs.elementary_charge * B / cs.proton_mass)

def electron_mobility(nu_e):
    """Electric mobility for electrons (mass transport)"""
    return (- cs.elementary_charge) / ( cs.electron_mass * nu_e)

def ion_mobility(nu_i):
    """Electric mobility for ions (mass transport)"""
    return (cs.elementary_charge) / ( cs.proton_mass * nu_i)

def electron_ratio(nu_e, B = 0.285e-04):
    """Electron ratio cyclotron frequency and collision"""
    return electron_cyclotron(B) / nu_e

def ion_ratio(nu_i, B = 0.285e-04):
    """Ion ratio cyclotron frequency and collision"""
    return ion_cyclotron(B) / nu_i



class conductivity:
    """Ionospheric conductivity given by Maeda 1977"""
    def __init__(
            self, 
            ne, 
            nue, 
            nui
            ):
        
        self.nue = nue
        self.ne = ne
        self.nue = nue
        self.nui = nui
        
        omega = gyrofrequency()
        
        self.omega_e = omega.electrons()
        self.omega_i = omega.ions()
    
    @property
    def R1(self):
        return ((self.omega_e / self.nue) * 
                (self.omega_i / self.nui))
    @property
    def R2(self):
        return self.R1**2 * self.nue**2 + self.omega_e**2
    
    @property    
    def parallel(self):
        """Parallel conductivity"""
        return ((self.ne * cs.elementary_charge**2) / 
                (cs.electron_mass * self.nue))
    @property
    def hall(self):
        """Hall conductivity on the field line"""
        return (self.parallel * self.omega_e * self.nue**2) / self.R2
    @property
    def pedersen(self):
        """Pedersen conductivity on the field line"""
        return (self.parallel * (1 + self.R1) * self.nue**2) / self.R2

class conductivity2:
    
    def __init__(
            self, 
            Ne, 
            nu_e, 
            nu_i, 
            B = 0.285e-04
            ):
        
        self.Ne = Ne
        self.nu_e = nu_e
        self.nu_i = nu_i
        self.B = B
        
    @property
    def parallel(self):
        """Along magnetic field (B)"""
        ion_term = 1 / ( cs.proton_mass * self.nu_i)
        electron_term  = 1 / ( cs.electron_mass * self.nu_e)
        return (self.Ne *  cs.elementary_charge**2 * 
                (electron_term + ion_term))
    
    @property
    def Pedersen(self): 
        """Along the electric field and perpendicular to B"""
        electron_term = (
            electron_mobility( self.nu_e) / 
            (1 + electron_ratio( self.nu_e, B = self.B)**2))
        
        ion_term = (ion_mobility( self.nu_i) / 
                    (1 + ion_ratio(self.nu_i, B = self.B)**2))
        
        return self.Ne * cs.elementary_charge * (ion_term - electron_term)
        
    @property
    def Hall(self):
        """Perpendicular to both electric and B"""
        
        electron_term = (
            electron_ratio( self.nu_e, B = self.B)**2 / 
            (1 + electron_ratio( self.nu_e, B = self.B)**2))
        
        ion_term = (ion_ratio( self.nu_i, B =  self.B)**2 / 
                    (1 + ion_ratio( self.nu_i, B =  self.B)**2))
        
        return (self.Ne * cs.elementary_charge / 
                self.B) * (electron_term - ion_term)




