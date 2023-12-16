import numpy as np 


def add_effective_winds(
        df,
        d = -19.62, 
        i = -6.04
        ):
    
    """Local case"""
    
    df['mer'] = df[['north', 'south']].mean(axis = 1)
    df['zon'] = df[['east', 'west']].mean(axis = 1)
    
    df = df.drop(
       columns = [
           'north', 'south', 
           'east', 'west'
           ]
       )

    wind = effective_wind()

    df['mer_perp'] = wind.meridional_perp(
       df['zon'], df['mer'], d, i
       )

    df['mer_parl'] = wind.meridional_parl(
       df['zon'], df['mer'], d, i
       )
    
    return df



class effective_wind(object):
    
    """
    Effective wind along and perpendicular of 
    magnetic field
    
     (Tese Ely, 2016; Nogueira, 2013)

    U_theta (mer) = 
    geographic meridional component (northward)
    U_phi (zon) = 
    geographiczonal component (eastward)
    
    """
    
    @staticmethod
    def zonal(zon, mer, D): 
        D = np.deg2rad(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def meridional_parl(zon, mer, D, I):
        """Componente paralela a B"""
        
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para norte)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.cos(I)
    
    @staticmethod
    def meridional_perp(zon, mer, D, I):
        """Componente perpendicular a B"""
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para norte)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.sin(I)



def winds_parameters(df):
    
    df.rename(
        columns = {"U": "zon", "V": "mer"}, 
        inplace = True
        )
        
    wind = effective_wind()
    
    df["zon_ef"] = wind.zonal(
        df["zon"], 
        df["mer"], 
        df["d"]
        )
    
    df["mer_perp"] = wind.meridional_perp(
        df["zon"], 
        df["mer"], 
        df["d"], 
        df["i"]
        )
    
    df["mer_parl"] = wind.meridional_parl(
        df["zon"], 
        df["mer"], 
        df["d"], 
        df["i"]
        )
    
    return df
