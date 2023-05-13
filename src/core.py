import pandas as pd
import ionosphere as io
from models import altrange_models
from atmosphere import recombination_rate



def compute_parameters(df) -> dict:
    
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
    
    cond = io.conductivity2(df["ne"], nue, nui)
    
    return {"perd": cond.pedersen, 
            "hall": cond.hall, 
            "parl": cond.parallel,
            "nui": nui, 
            "nue": nue}

def cond_from_models(**kwargs):
    
    """Compute conductivities from native models."""
    
    return pd.DataFrame(
        compute_parameters(
            altrange_models(**kwargs))
        )

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





def load_calculate(infile):

    df = pd.read_csv(infile, index_col = 0)
    
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
    
    df["R"] = recombination_rate(df["O2"], df["N2"])
    return df

infile = "D:\\FluxTube\\01\\201301010000.txt"


load_calculate(infile)
