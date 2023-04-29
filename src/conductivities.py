import scipy.constants as cs


class conductivity:
    """Ionospheric conductivity given by Kelley 2009"""
    def __init__(
            self, 
            B = 0.25e-04,
            mass = "effective"):
        
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
    
    def electron_mobility(self, nue):
        """Electric mobility for electrons (mass transport) (be)"""
        return (- self.charge) / (self.electron_mass * nue)
    
    def ion_mobility(self, nui):
        """Electric mobility for ions (mass transport) (bi)"""
        return (self.charge) / (self.ion_mass * nui)

    def electron_ratio(self, nue):
        """Ratio by Electron cyclotron and nue"""
        return self.electron_cyclotron / nue
    
    def ion_ratio(self, nui):
        """Ratio by ion cyclotron frequency and nui"""
        return self.ion_cyclotron / nui
    
    # testando para o caso de ki / 1 + ki^2
    def electron_term(self, ne, nue):
        """Electron part for compute pedersen conductivity"""
        return ((ne * self.charge / self.B) * 
                abs(self.electron_ratio(nue)) / (1 + pow(self.electron_ratio(nue), 2)))
    
    def ion_term(self, ne, nui):
        """Ion part for compute pedersen conductivity"""
        return ((ne * self.charge / self.B) *  
                self.ion_ratio(nui) / (1 + pow(self.ion_ratio(nui), 2)))
        
    def pedersen(self, ne, nui, nue): 
        """Along the electric field and perpendicular to B"""
        return self.electron_term(ne, nue) + self.ion_term(ne, nui)
            
    def pedersen_F(self, ne, nui):
        """
        For κi >> 1 (above 130 km) the Pedersen conductivity can
        be compute by (Sultan 1996)
        """
        return ne * self.ion_mass * nui / self.B**2
        
    def parallel(self, ne, nui, nue):
        """Along magnetic field (B)"""
        ion_term = 1 / (self.ion_mass * nui)
        electron_term = 1 / (self.electron_mass * nue)
        
        return (ne *  cs.elementary_charge**2 * (electron_term + ion_term))
    
    def hall(self, ne, nui, nue):
        """Perpendicular to both E and B"""
        
        electron_term = (
            self.electron_ratio(nue)**2 / (1 + self.electron_ratio(nue)**2)
            )
        
        ion_term = (
            self.ion_ratio(nui)**2 / (1 + self.ion_ratio(nui)**2)
            )
        
        return (ne * self.charge / self.B) * (electron_term - ion_term)




class conductivity2:
    """Ionospheric conductivity given by Maeda 1977"""
    def __init__(
            self, 
            ne, 
            nue, 
            nui,
            B = 0.25e-4, 
            mass = "effective"):
        
        self.ne = ne
        self.nue = nue
        self.nui = nui
        self.B = B

        
        if mass == "effective":
            # Effective mass of ions O+, O2+, NO+ in kg
            ions_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3
        else:
            ions_mass = cs.proton_mass
            
        self.ions_mass = ions_mass
        
        """Gyrofrequency for electrons in 1/s"""
        self.omega_e = cs.elementary_charge * self.B / cs.electron_mass
        self.omega_i = cs.elementary_charge * self.B / self.ions_mass 
        
    
    @property
    def R1(self):
        return ((self.omega_e / self.nue) * 
                (self.omega_i / self.nui))
    @property
    def R2(self):
        return (1 + self.R1)**2 * self.nue**2 + self.omega_e**2
    
    @property    
    def parallel(self):
        """Parallel conductivity"""
        return ((self.ne * cs.elementary_charge**2) / 
                (cs.electron_mass * self.nue))
    
    @property
    def pedersen(self):
        """Pedersen conductivity on the field line"""
        return (self.parallel * (1 + self.R1) * 
                self.nue**2 / self.R2)
    
    @property
    def hall(self):
        """Hall conductivity on the field line"""
        return (self.parallel * self.omega_e * 
                self.nue / self.R2)
