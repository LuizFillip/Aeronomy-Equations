import pandas as pd
import ionosphere as io
from models import altrange_models, point_msis
from utils import datetime_from_fn
import atmosphere as atm


def compute_parameters(df, B = 0.25e-04) -> dict:
    
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


import datetime as dt
from GEO import sites




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
    
    dn =  datetime_from_fn(infile)
    
    nu = io.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    df["nue"] = nu.electrons_neutrals2(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )
    
    mag = load_mag()
    
    B = mag[mag.index == dn]["F"].item()
    
    c = io.conductivity(B = B)

    df["perd"] = c.pedersen(
        df["Ne"], df["nui"], df["nue"]
        )
    
    df["R"] = atm.recombination2(df["O2"], df["N2"])
    
    df.rename(columns = {"U": "zon", "V": "mer"}, 
              inplace = True)
    #if dn is None:
    dn = datetime_from_fn(infile)
        
    return atm.fluxtube_eff_wind(df, dn)


def load_mag():

    df = pd.read_csv("mag.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    df = df.resample("10min").asfreq()
    
    df["F"] = df["F"] * 1e-9
    return df
    

def cond_from_models(ds, B = 0.25e-04):
    
    """Compute conductivities from in models."""
    
    return pd.DataFrame(compute_parameters(ds, B = B))
def timeseries():
    mag = load_mag()
    
    out = []
    
    for dn in mag.index:
    
        lat, lon = sites["saa"]["coords"]
            
        kwargs = dict(
              dn = dn, 
              glat = lat, 
              glon = lon,
              hmin = 150 
              )
        
        
        B = mag[mag.index == dn]["F"].item()
        
        ds =  cond_from_models(altrange_models(**kwargs), B = B)
        ds["alt"] = ds.index
        ds.index = [dn] * len(ds)
        out.append(ds)
        
    ts = pd.concat(out)
    
    
    ts.to_csv("conds.txt")
    
    

