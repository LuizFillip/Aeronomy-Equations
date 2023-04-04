import matplotlib.pyplot as plt
import numpy as np
from Models.src.core import neutral_iono_parameters
import datetime as dt


def plot_collision_freq(
        ax, 
        nu, 
        alts, 
        step = 50
        ):
    
    name = "Frequências de colisão"
    units = "$s^{-1}$"
    
    if nu.name == "nui":
        symbol = "$\\nu_{in}$"
    else:
        symbol = "$\\nu_{en}$"
        
    ax.plot(nu, alts,
            lw = 1, label = symbol)
    
    ax.legend()
    
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



def plot_profiles():
    
    
    fig, ax = plt.subplots(
        figsize = (6, 6),
        ncols = 2,
        sharey = True,
        dpi = 300
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    dn  = dt.datetime(2013, 1, 1)
    df = neutral_iono_parameters(
        dn  = dn, 
        hmin = 100
        )
    
    plot_collision_freq(
            ax[0], 
            df["nui"], 
            df.index)
    
    plot_collision_freq(
            ax[0], 
            df["nue"], 
            df.index)
    
    plot_local_conductivies(
            ax[1], 
            df["perd"], 
            df.index
            )
    
    plot_local_conductivies(
            ax[1], 
            df["hall"], 
            df.index
            )
    
    ax = plot_local_conductivies(
            ax[1], 
            df["par"], 
            df.index
            )
    
    ax.set(ylabel = "")
    fig.suptitle("São Luis - " + dn.strftime("%d/%m/%Y"))
    plt.show()
    
    return fig