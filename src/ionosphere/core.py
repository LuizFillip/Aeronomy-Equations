import aeronomy as ae
import GEO as gg
import pyIGRF 
import pandas as pd 

def magnetic_parameters(df):
    
    try:
        dn = df['dn'].values[0]
    except:
        dn = df.index[0]
        
    dn = pd.to_datetime(dn)
    
    dec = []
    inc = []
    total = []
    for lat, lon, alt in zip(df.glat, df.glon, df.alt):
        d, i, _, _, _, _, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = gg.year_fraction(dn)
            )
        
        dec.append(d)
        inc.append(i)
        total.append(f)
        
        
    df["d"] = dec
    df["i"] = inc
    df["Bf"] = total 
    
    df['Bf'] = df['Bf'] * 1e-9
        
    return df

def conductivity_parameters(df, other_conds = False):
    
    """
    Compute collision frequencies and 
    and ionospheric conductivities
    """


    nu = ae.collision_frequencies()

    df["nui"] = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )

    df["nue"] = nu.electrons_neutrals2(
        df["O"], 
        df["O2"], 
        df["N2"],
        df["He"], 
        df["H"],
        df["Te"]
        )

    df['perd'] = ae.conductivity(
        B = df['Bf'] 
        ).pedersen(
        df["ne"], 
        df["nui"], 
        df["nue"]
        )
    
    df['R'] = ae.recombination2(
        df["O2"], 
        df["N2"]
        )
            
    if other_conds:
            
        df['hall'] = ae.conductivity(
            B = df['Bf'] 
            ).hall(
            df["ne"], 
            df["nui"], 
            df["nue"]
            )
                
        df['parl'] = ae.conductivity(
            B = df['Bf'] 
            ).parallel(
            df["ne"], 
            df["nui"], 
            df["nue"]
            )

    


    return df
