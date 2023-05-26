import numpy as np

def scale_gradient(Ne, dz = 1, factor = 1e-3):
    """
    length scale gradient: Vertical variation of density
    
    Parameters:
        factor: convert km to meters
    """
    return np.gradient(np.log(Ne), dz, edge_order = 2)*factor

import pandas as pd
import matplotlib.pyplot as plt
from models import altrange_iri
from GEO import sites


df = pd.read_csv("iono_freqs.txt", index_col=0)
df.index = pd.to_datetime(df.index)
times = df.index.unique()

df["ne"] = 1.24e4 * df["freq"]**2

dn = times[12]

ds = df.loc[df.index == dn]



plt.plot(ds["ne"], ds["alt"])




lat, lon = sites["saa"]["coords"]

iri = altrange_iri(dn = dn, glat = lat, glon = lon, hmin = 75, 
                   hmax = 800)

plt.plot(iri["ne"]*1e-6, iri.index)

plt.show()
