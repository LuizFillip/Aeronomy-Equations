import scipy.constants as cs


class conductivity:
    """Ionospheric conductivity given by Kelley 2009"""
    def __init__(
            self, 
            Ne, 
            nue, 
            nui, 
            B = 0.25e-04,
            mass = "effective"):
        
        self.Ne = Ne
        self.nu_e = nue
        self.nu_i = nui
        self.B = B
        
        if mass == "effective":
            # Effective mass of ions O+, O2+, NO+ in kg
            ion_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3
        else:
            ion_mass = cs.proton_mass
            
        
        self.ion_mass = ion_mass
        self.electron_mass = cs.electron_mass
        self.charge = cs.elementary_charge
    
    @property
    def electron_cyclotron(self):
        """Electron gyro frequency"""
        return - (self.charge * self.B / self.electron_mass)
    
    @property
    def ion_cyclotron(self):
        """Ion gyro frequency"""
        return (self.charge * self.B / self.ion_mass)
    
    @property
    def electron_mobility(self):
        """Electric mobility for electrons (mass transport) (be)"""
        return (- self.charge) / (self.electron_mass * self.nu_e)
    
    @property
    def ion_mobility(self):
        """Electric mobility for ions (mass transport) (bi)"""
        return (self.charge) / (self.ion_mass * self.nu_i)

    @property
    def electron_ratio(self):
        """
        Ratio Electron cyclotron and eletron-nutral collision
        
        """
        return self.electron_cyclotron / self.nu_e
    
    @property
    def ion_ratio(self):
        """
        Ratio by ion cyclotron frequency and ion-neutral collision
        """
        return self.ion_cyclotron / self.nu_i
    
    
    @property
    def parallel(self):
        """Along magnetic field (B)"""
        ion_term = 1 / (self.ion_mass * self.nu_i)
        electron_term = 1 / (self.electron_mass * self.nu_e)
        
        return (self.Ne *  cs.elementary_charge**2 * 
                (electron_term + ion_term))
    
   
    @property
    def pedersen(self): 
        """Along the electric field and perpendicular to B"""
        
        electron_term = (
            self.electron_mobility / (1 + self.electron_ratio**2)
            )
        
        ion_term = (
            self.ion_mobility / (1 + self.ion_ratio**2)
            )
        
        return (
            self.Ne * self.charge * (ion_term - electron_term)
            )
    
    @property
    def pedersen_F(self):
        """
        For κi >> 1 (above 130 km) the Pedersen conductivity can
        be compute by
        """
        return self.Ne * self.ion_mass * self.nu_i / self.B**2
        
    @property
    def hall(self):
        """Perpendicular to both electric and B"""
        
        electron_term = (
            self.electron_ratio**2 / (1 + self.electron_ratio**2)
            )
        
        ion_term = (
            self.ion_ratio**2 / (1 + self.ion_ratio**2)
            )
        
        return (self.Ne * self.charge / 
                self.B) * (electron_term - ion_term)




class conductivity2:
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
        
       
        
        self.omega_e = self.electrons()
        self.omega_i = self.ions()
        
        
    #default: Equatorial geomagnetic field in Tesla
    @staticmethod
    def ions(B = 0.25e-4, mass = "effective"):
        """Gyrofrequency for ions in 1/s"""
        
        if mass == "effective":
            # Effective mass of ions O+, O2+, NO+ in kg
            ions_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3
        else:
            ions_mass = cs.proton_mass
            
        return cs.elementary_charge * B / ions_mass 
    
    @staticmethod
    def electrons(B = 0.25e-4):
        """Gyrofrequency for electrons in 1/s"""
        return  cs.elementary_charge * B / cs.electron_mass
    
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
        return (self.parallel * self.omega_e * 
                self.nue**2) / self.R2
    @property
    def pedersen(self):
        """Pedersen conductivity on the field line"""
        return (self.parallel * (1 + self.R1) * 
                self.nue**2) / self.R2
