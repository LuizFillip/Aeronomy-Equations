from models import altrange_iri, altrange_msis
import datetime as dt
from GEO import sites
import pandas as pd
import ionosphere as io
import matplotlib.pyplot as plt


glat, glon = sites["saa"]["coords"]

kargs = dict(
    dn = dt.datetime(2013, 1, 1, 21), 
    glat = glat, 
    glon = glon
    )


def get_data(**kargs):
    
    iri = altrange_iri(**kargs)
    
    msi = altrange_msis(**kargs)
    
    return pd.concat([msi, iri], axis = 1)

df = get_data(**kargs)


def compute_collisions(df):
    
    nui = io.ion_neutral()
    
    nui = nui.BB1996(
        df["Tn"], 
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    
    nui2 = io.collision_frequencies()
    
    nue = nui2.electrons_neutrals(
        df["O"], 
        df["O2"],
        df["N2"],
        df["He"],
        df["H"],
        df["Te"]
    )
    
    return nui, nue



