import pandas as pd
import ionosphere as io
from base import Filename2dn
import atmosphere as atm



def compute_parameters(
        df, 
        B = 0.25e-04) -> dict:
    
    """
    Compute collision frequencies and 
    and ionospheric conductivities
    """
    
    nu = io.collision_frequencies()
    
    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    nue = nu.electrons_neutrals(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )
    
    c = io.conductivity(B = B)

    df["perd"] = c.pedersen(
        df["ne"], nui, nue
        )
    
    df["hall"] = c.hall(
        df["ne"], nui, nue
        )
        
    return df



def cond_from_file(
        infile = "pyglow_south.txt", 
        order = 1e6           
        ):
    
    df =  pd.read_csv(infile, index_col = 0)
        
    df["ne"] = df["ne"] * order
 
    ds = pd.DataFrame(compute_parameters(df))
    
    for col in list(df.columns)[:6]:
        ds[col] = df[col].copy()
        
    return ds[list(ds.columns)[::-1]]


def load_calculate(infile, dn = None):

    df = pd.read_csv(infile, index_col = 0)
    
    dn =  Filename2dn(infile)
    
    nu = io.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    df["nue"] = nu.electrons_neutrals2(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )

    c = io.conductivity()

    df["perd"] = c.pedersen(
        df["Ne"], df["nui"], df["nue"]
        )
    
    df["R"] = atm.recombination2(df["O2"], df["N2"])
    
    df.rename(columns = {"U": "zon", "V": "mer"}, 
              inplace = True)
   
    dn = Filename2dn(infile)
        
    return atm.fluxtube_eff_wind(df, dn)




