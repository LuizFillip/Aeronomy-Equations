import datetime as dt
from GEO import sites
import pandas as pd
import ionosphere as io
from models import get_data

def compute_parameters(df) -> dict:
    
    nu = io.collision_frequencies()
    
    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    nue = nu.electrons_neutrals(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )
    
    cond = io.conductivity(df["ne"], nue, nui)
    

    return {"perd": cond.pedersen, 
            "hall": cond.hall, 
            "parl": cond.parallel,
            "nui": nui, 
            "nue": nue}

def get_conductivity(**kwargs):
    return pd.DataFrame(
        compute_parameters(
            get_data(**kwargs))
        )


def main():

    glat, glon = sites["saa"]["coords"]
    
    kwargs = dict(
        dn = dt.datetime(2013, 1, 1, 21), 
        glat = glat, 
        glon = glon,
        hmin = 200 
        )
    
    ds = get_conductivity(**kwargs)
    

