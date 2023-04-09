import matplotlib.pyplot as plt
import numpy as np
from Models.src.core import neutral_iono_parameters
import datetime as dt

def plot_local_conductivies(
        ax, 
        nu, 
        alts, 
        step = 50
        ):
    
    name = "Condutividades locais"
    units = "mho"
    
    if nu.name == "perd":
        symbol = "$\sigma_{P}$"
    elif nu.name == "hall":
        symbol = "$\sigma_{H}$"
    else:
        symbol = "$\sigma_{0}$"
        
    ax.plot(nu, alts,
            lw = 1, label = symbol)
    
    ax.legend(loc = "upper right")
    
    ax.set(
        xscale = "log", 
        yticks = np.arange(
            min(alts), 
            max(alts) + step, 
            step),
        ylim = [min(alts), max(alts)],
        xlabel = f"{name} ({units})",
        ylabel = "Altitude (km)"
        )
    return ax

def quick_view():
    
     fig, ax = plt.subplots(
         dpi = 300
         )

     dn  = dt.datetime(2013, 1, 1)
     df = neutral_iono_parameters(
        dn  = dn, 
        hmin = 100
        )
    
     plot_local_conductivies(
            ax, 
            df["perd"], 
            df.index
            )
    
     plot_local_conductivies(
            ax, 
            df["hall"], 
            df.index
            )
    
     ax = plot_local_conductivies(
            ax, 
            df["par"], 
            df.index
            )
     
quick_view()