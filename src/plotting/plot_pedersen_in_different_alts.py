import matplotlib.pyplot as plt
from ionosphere import conductivity, test_data
import datetime as dt
from GEO import sites
import pytest
import pandas as pd



def plot_pedersen_in_different_alts():
    
    glat, glon = sites["saa"]["coords"]

    kwargs = dict(
        dn = dt.datetime(2013, 1, 1, 21), 
        glat = glat, 
        glon = glon,
        hmin = 75,
        hmax = 300
        )

    ds = test_data(**kwargs)

    c = conductivity()

    ds_lower = ds.loc[ds.index <= 100].copy()
        
    ds_lower["perd"] = c.electron_term(ds["ne"], ds["nue"])
    
    ds_upper = ds.loc[(ds.index >= 100) & (ds.index <= 150)].copy()
    
    ds_upper["perd"] = c.ion_term(ds["ne"], ds["nui"])
    
    region_E = pd.concat([ds_lower, ds_upper])
    
    
    lower_F = ds.loc[(ds.index >= 130)].copy()
    
    lower_F["perd"] = c.pedersen_F(lower_F["ne"], lower_F["nui"])
    
    ds["perd"] = c.pedersen(ds["ne"], ds["nui"], ds["nue"])
    
    fig = plt.figure(dpi = 300)
        
    plt.plot(ds["perd"], ds.index, label = "total")
    plt.plot(lower_F["perd"], lower_F.index, label = "$> 130$")
    plt.plot(ds_lower["perd"], ds_lower.index, label = "$< 100$")
    plt.plot(ds_upper["perd"], ds_upper.index, label = " $>100$ e $<150$")
    
    plt.xscale("log")
    plt.xlabel("$\sigma_P$ (ohms)")
    plt.ylabel("Altitude (km)")
    plt.legend()